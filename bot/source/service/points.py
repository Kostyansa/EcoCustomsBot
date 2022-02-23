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

    def add(self, userid, points):
        self.pointsRepository.add(userid, points)

    def get(self, userid):
        return self.pointsRepository.getForUser(userid)