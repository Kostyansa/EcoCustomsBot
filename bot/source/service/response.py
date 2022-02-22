import functools
import logging
from sre_constants import SUCCESS
import time
from concurrent import futures
from urllib import response
from entity.event import Event
from entity.response import Response
import qrcode

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Update

from config.config import ABOUT, BALANCE, COMMAND_NOT_FOUND, DO_NOT_KNOW, EVENT, GENERIC_ERROR, NOT_ENOUGH_POINTS, POINTS, EVENTS, START, USER_NOT_FOUND, USER_NOT_REGISTERED

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
            [ABOUT],
            [POINTS],
            [EVENTS]
        ]
        response.replyMarkup = ReplyKeyboardMarkup(keyboard)
        return response

    def about(self):
        response = Response(ABOUT)
        return response

    def doNotKnow(self):
        response = Response(DO_NOT_KNOW)
        return response

    def notRegistered(self):
        response = Response(USER_NOT_REGISTERED)
        return response

    def points(self, user, points):
        response = Response(BALANCE.format(points))
        response.photo = qrcode.make(user.telegram_id).make_image()
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

    def events(self, events):
        response = Response(EVENTS)
        keyboard = []
        for event in events:
            keyboard.append(InlineKeyboardButton(event.name, callback_data=f"event {event.id}"))
        return response

    def generic_error(self, error):
        response = Response(GENERIC_ERROR.format(error))
        return response

