from datetime import datetime, timedelta
import os
import time
import logging
from urllib import response
import uuid

from entity.user import User
from service.event import EventService
from service.response import ResponseService
from service.user import UserService
from service.points import PointsService
from entity.event import Event
from entity.user import Role

from config.config import ABOUT, POINTS, EVENTS


class Controller:

    admin_key = str(uuid.uuid4())

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
                return self.responseService.points(user, points)
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
                user = self.userService.get(userid)
                if user.role == Role.ADMIN:
                    return self.responseService.eventAdmin(event)
                else:
                    return self.responseService.event(event)
            else:
                return self.responseService.doNotKnow()
        elif text == self.admin_key:
            if self.admin_key:
                self.admin_key = None
                user = self.userService.get(userid)
                self.userService.elevate(user)
                return self.responseService.success()
        else:
            event = self.eventService.checkCode(text)
            if event:
                self.eventService.addVisited(user, event)
                self.pointsService.add(user.id, event.amount)
                return self.responseService.success()
            else:
                return self.responseService.doNotKnow()

    def onCommandStart(self, userid):
        user = self.userService.get(userid)
        if user is None:
            user = User(None, userid, None)
            self.userService.save(user)
        response = self.responseService.start()
        return response

    def onCommandEvents(self):
        events = self.eventService.getAll()
        if len(events) > 0:
            return self.responseService.events(events)
        else:
            return self.responseService.noEvents()

    def onCommandAdd(self, userid, target, amount):
        user = self.userService.get(userid)
        if user.role == Role.ADMIN:
            try:
                amount = int(amount)
                target = self.userService.get(target)
                if target is not None:
                    self.pointsService.add(target, amount)
                    return self.responseService.success()
                else:
                    return self.responseService.userNotFound()
            except ValueError:
                return self.responseService.generic_error("Ошибка в аргументах")
        else:
            return self.responseService.commandNotFound()

    def onCommandPromote(self, userid, target):
        user = self.userService.get(userid)
        if user.role == Role.ADMIN:
            try:
                target = self.userService.get(target)
                if target is not None:
                    self.userService.elevate(target)
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
                event = Event(None, name, str(uuid.uuid4())[0:7], int(amount), datetime.strptime(date, "%d.%m.%YT%H:%M"), description)
                self.eventService.add(event)
                return self.responseService.success()
            except ValueError:
                return self.responseService.generic_error("Ошибка в аргументах")
        else:
            return self.responseService.commandNotFound()