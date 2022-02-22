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
        self.eventRepository.add()

    def get(self):
        return self.eventRepository.get()