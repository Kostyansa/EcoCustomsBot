import time
import uuid
import threading
import os
import logging
import sys
import json

from sqlalchemy import create_engine

import repository.database
from entity.response import Response
from factory.service_factory import ServiceFactory
from telegram.error import NetworkError, Unauthorized, TelegramError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext

from controller import Controller

class AdapterTelegram:

    def __init__(self, APIKey, controller : Controller):
        self.controller = controller
        self.updater = Updater(token = APIKey, use_context=True)
        self.bot = self.updater.bot
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CommandHandler('events', self.events))
        self.updater.dispatcher.add_handler(CommandHandler('add', self.add))
        self.updater.dispatcher.add_handler(CommandHandler('withdraw', self.withdraw))
        self.updater.dispatcher.add_handler(CommandHandler('add_event', self.add_event))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.on_message))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.on_callback))
        self.updater.dispatcher.add_error_handler(self.error_handler)

    def start(self, update, context) -> None:
        logging.info(f'Start command from {update.message.chat.id}')
        response = self.controller.onCommandStart(update.message.chat.id)
        self.send_response(update.message.chat.id, response)

    def events(self, update, context) -> None:
        logging.info(f'Events command from {update.message.chat.id}')
        response = self.controller.onCommandEvents(update.message.chat.id)
        self.send_response(update.message.chat.id, response)

    def add(self, update, context : CallbackContext) -> None:
        logging.info(f'Events command from {update.message.chat.id}')
        args = context.args
        response = self.controller.onCommandAdd(update.message.chat.id, args[0], args[1], args[2])
        self.send_response(update.message.chat.id, response)

    def withdraw(self, update, context : CallbackContext) -> None:
        logging.info(f'Events command from {update.message.chat.id}')
        args = context.args
        response = self.controller.onCommandWithdraw(update.message.chat.id, args[0], args[1], args[2])
        self.send_response(update.message.chat.id, response)

    def add_event(self, update, context : CallbackContext) -> None:
        logging.info(f'Events command from {update.message.chat.id}')
        args = context.args
        response = self.controller.onCommandAddEvent(update.message.chat.id, args[0], args[1], args[2], (" ").join(args[3:]))
        self.send_response(update.message.chat.id, response)

    def error_handler(self, update, context) -> None:
        logging.warning(f'Error while sendind message', exc_info=context.error)
        if update is not None:
            if update.message is not None:
                if update.message.chat is not None:
                    self.bot.send_message(update.message.chat.id, "Во время обработки вашего сообщения произошла ошибка, пожалуйста, попробуйте позже.")

    def send_response(self, chat_id, response : Response):
        if response.replyMarkup:
            self.bot.send_message(chat_id, response.message, response.replyMarkup)
        else:
            self.bot.send_message(chat_id, response.message)
        if response.photo:
            self.bot.send_photo(chat_id, response.photo)

    def on_message(self, update, context) -> None:
        logging.info(f'Got message from {update.message.chat.id}')
        logging.debug(f'Message: {update.message.text}')
        response = self.on_message(update.message.text, update.message.chat.id)
        self.send_response(update.message.chat.id, response)
        logging.info(f'Sent response to {update.message.chat.id}')

    def on_callback(self, update, context) -> None:
        query = update.callback_query
        logging.info(f'Got callback message from {query.message.chat.id}')
        logging.debug(f'Got message: {query.data}')
        query.answer()
        response = self.on_message(query.data, query.message.chat.id)
        self.send_response(query.message.chat.id, response)
        logging.info(f'Send response to {query.message.chat.id}')

    def on_message(self, update, context):
        self.corr_id = str(uuid.uuid4())
        return self.controller.onMessage(update.message.chat.id, update.message.text)

    def telegram_start(self):
        self.updater.start_polling()

    def start(self) -> None:
        self.telegram_start()


def main():
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', encoding='utf-8', level=logging.DEBUG)
    DB_URL = os.environ.get('DB_URL')
    api_key = os.environ.get('API_KEY')
    engine = create_engine(DB_URL, echo=False)
    repository.database.init_database(engine)
    service_factory = ServiceFactory()
    response_service = service_factory.getResponseService()
    user_service = service_factory.getUserService()
    controller = Controller(response_service, user_service)
    telegram = AdapterTelegram(api_key, controller)
    telegram.start()

if __name__ == "__main__":
    main()