import functools
import logging
import time
from concurrent import futures
from urllib import response
from entity.response import Response

from repository.response import ResponseRepository

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Update

class ResponseService:

    def __init__(
            self, 
            responseRepository : ResponseRepository
        ):
        self.responseRepository = responseRepository

    def onMessage(self, message):
        pass

    def start(self):
        response = Response("Start response", )
        pass

    def success(self):
        pass

    def userNotFound(self):
        pass

    def commandNotFound(self):
        pass

    def notEnoughPoints(self):
        pass

    def events(self, events):
        pass

