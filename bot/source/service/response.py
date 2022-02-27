import functools
import logging
import time
from concurrent import futures
from entity.event import Event
from entity.response import Response
import qrcode
import io

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Update

from config.config import ABOUT_BUTTON, BALANCE, COMMAND_NOT_FOUND, DO_NOT_KNOW, EVENT, GENERIC_ERROR, NOT_ENOUGH_POINTS, POINTS, EVENTS, START, USER_NOT_FOUND, USER_NOT_REGISTERED, NO_EVENTS, HELP, HELP_ADMIN, USERS, SUCCESS, NOT_STARTED, EVENT_ADMIN

class ResponseService:

    def __init__(
            self
        ):
        pass

    def onMessage(self, message):
        pass

    def start(self):
        response = Response(START)
        keyboard = [
            [ABOUT_BUTTON],
            [POINTS],
            [EVENTS]
        ]
        response.replyMarkup = ReplyKeyboardMarkup(keyboard)
        return response

    def about(self):
        response = Response(ABOUT_BUTTON)
        return response

    def doNotKnow(self):
        response = Response(DO_NOT_KNOW)
        return response

    def notRegistered(self):
        response = Response(USER_NOT_REGISTERED)
        return response

    def points(self, user, points):
        response = Response(BALANCE.format(points))
        qr = qrcode.QRCode()
        qr.add_data(user.telegram_id)
        img = qr.make_image()
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        byte_im = buf.getvalue()
        response.photo = byte_im
        return response

    def success(self):
        response = Response(SUCCESS)
        return response

    def userNotFound(self):
        response = Response(USER_NOT_FOUND)
        return response

    def commandNotFound(self):
        response = Response(COMMAND_NOT_FOUND)
        return response

    def notEnoughPoints(self):
        response = Response(NOT_ENOUGH_POINTS)
        return response

    def event(self, event : Event):
        response = Response(EVENT.format(event.name, event.date, event.description))
        return response

    def eventAdmin(self, event : Event):
        response = Response(EVENT_ADMIN.format(event.id, event.name, event.date, event.description))
        qr = qrcode.QRCode()
        qr.add_data(event.code)
        img = qr.make_image()
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        byte_im = buf.getvalue()
        response.photo = byte_im
        return response

    def events(self, events):
        response = Response(EVENTS)
        keyboard = []
        for event in events:
            keyboard.append([InlineKeyboardButton(event.name, callback_data=f"event {event.id}")])
        response.replyMarkup = InlineKeyboardMarkup(keyboard)
        return response

    def noEvents(self):
        response = Response(NO_EVENTS)
        return response

    def generic_error(self, error):
        response = Response(GENERIC_ERROR.format(error))
        return response

    def help(self):
        response = Response(HELP)
        return response

    def help_admin(self):
        response = Response(HELP_ADMIN)
        return response

    def users(self, users):
        response = Response(USERS)
        keyboard = []
        for user in users:
            keyboard.append([InlineKeyboardButton(f'Id:{user.telegram_id}, Points:{user.points}', callback_data=f"user {user.id}")])
        response.replyMarkup = InlineKeyboardMarkup(keyboard)
        return response

    def alreadyUsed(self):
        response = Response(NOT_STARTED)
        return response


