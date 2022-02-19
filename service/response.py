import functools
import logging
import time
from concurrent import futures

from repository.response import ResponseRepository

class ResponseService:

    def __init__(
            self, 
            responseRepository : ResponseRepository
        ):
        self.responseRepository = responseRepository