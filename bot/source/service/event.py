import functools
import logging
import time
from concurrent import futures

from repository.event import EventRepository

class EventService:

    def __init__(
            self, 
            eventRepository : EventRepository
        ):
        self.eventRepository = eventRepository

    def add(self, event):
        self.eventRepository.add(event)

    def getAll(self):
        return self.eventRepository.getAll()

    def get(self, id):
        return self.eventRepository.get(id)

    def checkCode(self, code):
        return self.eventRepository.checkCode(code)

    def addVisited(self, user, event):
        self.eventRepository.visited(user, event)