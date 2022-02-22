import os

from repository.event import EventRepository
from repository.points import PointsRepository
from repository.user import UserRepository

from sqlalchemy import create_engine

class RepositoryFactory:

    _instance = None

    def __init__(self):    
        DB_HOST = os.environ.get('DBHOST')
        DB_USER = os.environ.get('POSTGRES_USER')
        DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
        DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/postgres'
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
    