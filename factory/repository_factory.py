import os

from repository.response import ResponseRepository # pylint: disable=import-error
from repository.user import UserRepository # pylint: disable=import-error

class RepositoryFactory:

    _instance = None

    def __init__(self):
        self.engine = None
        self.responseRepository = ResponseRepository(self.engine)
        self.userRepository = UserRepository(self.engine)

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getResponseRepository(self):
        return self.responseRepository

    def getUserRepository(self):
        return self.userRepository
    