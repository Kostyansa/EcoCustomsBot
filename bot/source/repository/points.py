from sqlalchemy.engine import Engine

from sqlalchemy.sql import text

class PointsRepository:
    def __init__(self, engine : Engine) -> None:
        self.engine = engine

    def add(self, user, amount):
        self.engine.execute(
            text('''
            INSERT INTO user_points(user_id, points)
            VALUES(:user_id, :points)
            '''),
            user_id = user.id,
            points = amount
        )

    def getForUser(self, user):
        points = self.engine.execute(
            text('''
            SELECT COALESCE(SUM(points), 0) as sum
            FROM user_points
            WHERE user_id = :user_id
            GROUP BY user_id
            '''),
            user_id = user.id
        ).fetchone()
        if points:
            return points['sum']
        else:
            return 0
