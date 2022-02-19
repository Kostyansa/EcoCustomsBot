import os
import time
import logging
import uuid

from entities.message import Message
from service.response import ResponseService
from service.user import UserService

class Controller:

    def __init__(self, responseService : ResponseService, userService : UserService):
        self.responseService = responseService
        self.userService = userService


    def onMessage(self, message):
        response = self.responseService.getResponseByMessage(message)
        return response

    def onCommandStart(self, userid):
        self.userService.save(userid)
        message = Message(userid, "start")
        response = self.responseService.getResponseByMessage(message)
        return response

