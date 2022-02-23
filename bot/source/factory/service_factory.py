from factory.repository_factory import RepositoryFactory

from service.response import ResponseService
from service.user import UserService
from service.event import EventService
from service.points import PointsService

class ServiceFactory:

    _instance = None

    def __init__(self):
        self.repositoryFactory = RepositoryFactory.getInstance()
        self.userService = UserService(self.repositoryFactory.getUserRepository())
        self.responseService = ResponseService()
        self.eventService = EventService(self.repositoryFactory.getEventRepository())
        self.pointsService = PointsService(self.repositoryFactory.getPointsRepository())
        

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getUserService(self):
        return self.userService

    def getResponseService(self):
        return self.responseService

    def getEventService(self):
        return self.eventService

    def getPointsService(self):
        return self.pointsService


    