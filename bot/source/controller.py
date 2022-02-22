from datetime import datetime, timedelta
import os
import time
import logging
from urllib import response
import uuid

from service.event import EventService
from service.response import ResponseService
from service.user import UserService
from service.points import PointsService
from entity.event import Event
from entity.user import Role

from config.config import ABOUT, POINTS, EVENTS

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
        if text == POINTS:
            user = self.userService.get(userid)
            if user is not None:
                points = self.pointsService.get(user.id)
                return self.responseService.points(points)
            else:
                return self.responseService.notRegistered()
        elif text == ABOUT:
            return self.responseService.about()
        elif text == EVENTS:
            return self.onCommandEvents()
        elif text.startswith("event "):
            event_id = int(text.split(" ")[1])
            event = self.eventService.get(event_id)
            if event is not None:
                return self.responseService.event(event)
            else:
                return self.responseService.doNotKnow()
        else:
            event = self.eventService.checkCode(text)
            if event:
                self.eventService.addVisited(user, event)
                self.pointsService.add(user.id, event.amount, datetime.now() + timedelta(days=2))
                return self.responseService.success()
            else:
                return self.responseService.doNotKnow()

    def onCommandStart(self, userid):
        user = self.userService.get(userid)
        if user is not None:
            self.userService.save(userid)
        response = self.responseService.start(userid)
        return response

    def onCommandEvents(self):
        events = self.eventService.getAll()
        return self.responseService.events(events)

    def onCommandAdd(self, userid, target, amount, expiration_date):
        user = self.userService.get(userid)
        if user.role == Role.ADMIN:
            try:
                amount = int(amount)
                expiration_date = datetime.strptime(expiration_date, "%d.%m.%Y")
                target = self.userService.get(target)
                if target is not None:
                    self.pointsService.add(target, amount, expiration_date)
                    return self.responseService.success()
                else:
                    return self.responseService.userNotFound()
            except ValueError:
                return self.responseService.generic_error("Ошибка в аргументах")
        else:
            return self.responseService.commandNotFound()

    def onCommandWithdraw(self, userid, target, amount):
        user = self.userService.get(userid)
        if user.role == Role.ADMIN:
            try:
                amount = int(amount)
                expiration_date = datetime.strptime(expiration_date, "%d.%m.%Y")
                target = self.userService.get(target)
                if target is not None:
                    if self.pointsService.get(userid) >= amount:
                        self.pointsService.add(target, -amount)
                        return self.responseService.success()
                    else:
                        return self.responseService.notEnoughPoints()
                else:
                    return self.responseService.userNotFound()
            except ValueError:
                return self.responseService.generic_error("Ошибка в аргументах")
        else:
            return self.responseService.commandNotFound()

    def onCommandAddEvent(self, userid, name, date, amount, description):
        user = self.userService.get(userid)
        if user.role == Role.ADMIN:
            try:
                event = Event(None, name, uuid.uuid4[0:7], int(amount), datetime.strptime(date, "%d.%m.%Y"), description)
                self.eventService.add(event)
                return self.responseService.success()
            except ValueError:
                return self.responseService.generic_error("Ошибка в аргументах")
        else:
            return self.responseService.commandNotFound()