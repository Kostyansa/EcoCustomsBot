import os

from repository.event import EventRepository
from repository.points import PointsRepository
from repository.user import UserRepository

from sqlalchemy import create_engine

class RepositoryFactory:

    _instance = None

    def __init__(self):
        DB_URL = os.environ.get('DB_URL')
        engine = create_engine(DB_URL, echo=False)
        self.eventRepository = EventRepository(self.engine)
        self.userRepository = UserRepository(self.engine)
        self.pointsRepository = PointsRepository(self.engine)

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getEventRepository(self):
        return self.eventRepository

    def getPointsRepository(self):
        return self.pointsRepository

    def getUserRepository(self):
        return self.userRepository
    