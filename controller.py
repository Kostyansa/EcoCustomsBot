import os
import time
import logging
import uuid

from service.event import EventService
from service.response import ResponseService
from service.user import UserService
from service.points import PointsService
from entity.event import Event

admin_key = uuid.uuid4()

class Controller:

    def __init__(self, 
    responseService : ResponseService, 
    userService : UserService, 
    pointsService : PointsService,
    eventService: EventService
    ):
        self.responseService = responseService
        self.userService = userService
        self.pointsService = pointsService
        self.eventService = eventService

    def onMessage(self, userid, text):
        response = self.responseService.onMessage(userid, text)
        return response

    def onCommandStart(self, userid):
        user = self.userService.get(userid)
        if user is not None:
            self.userService.save(userid)
        response = self.responseService.start(userid)
        return response

    def onCommandAdd(self, userid, target, amount, expiration_date):
        user = self.userService.get(userid)
        if user.role == "ADMIN":
            target = self.userService.get(target)
            if target is not None:
                self.pointsService.add(target, amount, expiration_date)
                return self.responseService.success()
            else:
                return self.responseService.userNotFound()
        else:
            return self.responseService.commandNotFound()

    def onCommandWithdraw(self, userid, target, amount):
        user = self.userService.get(userid)
        if user.role == "ADMIN":
            target = self.userService.get(target)
            if target is not None:
                if self.pointsService.get(userid) >= amount:
                    self.pointsService.add(target, -amount)
                    return self.responseService.success()
                else:
                    return self.responseService.notEnoughPoints()
            else:
                return self.responseService.userNotFound()
        else:
            return self.responseService.commandNotFound()

    def onCommandEvents(self):
        events = self.eventService.get()
        return self.responseService.events(events)

    def onCommandAddEvent(self, userid, name, date, amount, description):
        user = self.userService.get(userid)
        if user.role == "ADMIN":
            event = Event(None, name, uuid.uuid4[0:7], amount, date, description)
            pass
        else:
            return self.responseService.commandNotFound()