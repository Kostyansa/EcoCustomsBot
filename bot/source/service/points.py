import functools
import logging
import time
from concurrent import futures

from repository.points import PointsRepository

class PointsService:

    def __init__(
            self, 
            pointsRepository : PointsRepository
        ):
        self.pointsRepository = pointsRepository

    def add(self, user, points):
        self.pointsRepository.add(user, points)

    def get(self, user):
        return self.pointsRepository.getForUser(user)