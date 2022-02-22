from factory.repository_factory import RepositoryFactory

from service.response import ResponseService # pylint: disable=import-error
from service.user import UserService # pylint: disable=import-error

class ServiceFactory:

    _instance = None

    def __init__(self):
        self.repositoryFactory = RepositoryFactory.getInstance()
        self.userService = UserService(self.repositoryFactory.getUserRepository())
        self.responseService = ResponseService(self.repositoryFactory.getResponseRepository())

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getUserService(self):
        return self.userService

    def getResponseService(self):
        return self.responseService

    