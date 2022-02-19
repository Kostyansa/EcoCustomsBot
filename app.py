import time
import uuid
import threading
import os
import logging
import sys
import json

from telegram.error import NetworkError, Unauthorized, TelegramError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext

from controller import Controller

class AdapterTelegram:

    def __init__(self, APIKey, controller : Controller):

        self.controller = controller

        self.updater = Updater(token = APIKey)
        self.bot = self.updater.bot
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start_command))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.echo))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.callback_echo))
        self.updater.dispatcher.add_error_handler(self.error_handler)



    def start_command(self, update, context) -> None:
        logging.info(f'Start message from {update.message.chat.id}')
        response = self.controller.onCommandStart(update.message.chat.id)
        self.send_response(update.message.chat.id, response)

    def error_handler(self, update, context) -> None:
        logging.warning(f'Error while sendind message', exc_info=context.error)
        if update is not None:
            if update.message is not None:
                if update.message.chat is not None:
                    self.bot.send_message(update.message.chat.id, "Во время обработки вашего сообщения произошла ошибка, пожалуйста, попробуйте позже.")


    def prepare_inline_keyboard(self, keyboard):
        if keyboard.row_width:
            row_width = int(keyboard.row_width)
        else:
            row_width = 1
        result = []
        keys = keyboard.keys
        for i in range(len(keys)//row_width + 1):
            row_keys = keys[i*row_width:(i+1)*row_width]
            row = []
            for key in row_keys:
                if key.url:
                    row.append(InlineKeyboardButton(key.label, url = key.url))
                elif key.callback_data:
                    row.append(InlineKeyboardButton(key.label, callback_data = key.callback_data))
                else:
                    row.append(InlineKeyboardButton(key.label, callback_data = key.label))
            result.append(row)
        return result

    def prepare_reply_keyboard(self, keyboard):
        if keyboard.row_width:
            row_width = int(keyboard.row_width)
        else:
            row_width = 1
        result = []
        keys = keyboard.keys
        for i in range(len(keys)//row_width + 1):
            row_keys = keys[i*row_width:(i+1)*row_width]
            row = []
            for key in row_keys:
                row.append(key.label)
            result.append(row)
        return result

    def send_response(self, chat_id, response):
        if response.keyboard:
            keyboard = response.keyboard
            if keyboard.type == 'InlineKeyboard':
                    reply_markup = InlineKeyboardMarkup(self.prepare_inline_keyboard(keyboard))
            elif keyboard.type == 'ReplyKeyboard':
                    reply_markup = ReplyKeyboardMarkup(self.prepare_reply_keyboard(keyboard))
            else:
                reply_markup = InlineKeyboardMarkup(self.prepare_inline_keyboard(keyboard))

            if response.message:
                self.bot.send_message(chat_id, response.message, reply_markup=reply_markup)
            else:
                self.bot.send_message(chat_id, response.name, reply_markup=reply_markup)
        else:
            self.bot.send_message(chat_id, response.message)
        if response.pictures:
            for picture in response.pictures:
                self.bot.send_photo(chat_id, picture.URL)
        if response.location:
            self.bot.send_location(chat_id, float(response.location.latitude), float(response.find.location.longitude))



    def echo(self, update, context) -> None:
        start_time = time.time_ns()
        logging.info(f'Got message from {update.message.chat.id}')
        logging.debug(f'Message: {update.message.text}')
        response = self.call(update.message.text, update.message.chat.id)
        logging.debug(f'Sending response: {response.name}')
        logging.debug(f'Build a response in {(time.time_ns() - start_time)/1000000}')
        self.send_response(update.message.chat.id, response)
        logging.info(f'Sent response to {update.message.chat.id}')
        logging.debug(f'Responded in {(time.time_ns() - start_time)/1000000}')

    def callback_echo(self, update, context) -> None:
        start_time = time.time_ns()
        query = update.callback_query
        logging.info(f'Got callback message from {query.message.chat.id}')
        logging.debug(f'Got message: {query.data}')
        query.answer()
        response = self.call(query.data, query.message.chat.id)
        logging.debug(f'Sending response: {response.name}')
        logging.debug(f'Build a response in {(time.time_ns() - start_time)/1000000}')
        self.send_response(query.message.chat.id, response)
        logging.info(f'Send response to {query.message.chat.id}')
        logging.debug(f'Responded in {(time.time_ns() - start_time)/1000000}')

    def call(self, message, chat_id):
        self.corr_id = str(uuid.uuid4())
        message_entity = Message(source, str(chat_id), message)
        return self.controller.onMessage(message_entity)

    def telegram_start(self):
        self.updater.start_polling()

    def start(self) -> None:
        self.telegram_start()

