from sqlalchemy.engine import Engine

class PointsRepository:
    def __init__(self, engine : Engine) -> None:
        self.engine = engine

    def add(self, userid, amount, expiration_date):
        self.engine.execute(
            '''
            INSERT INTO user_points(user_id, points, until)
            VALUES(:user_id, :points, :until)
            ''',
            user_id = userid,
            points = amount,
            until = expiration_date
        )

    def getForUser(self, userid):
        points = self.engine.execute(
            '''
            SELECT SUM(points) as sum
            FROM user_points 
            WHERE (expiration_date >= NOW()) or (expiration_date is NULL)
            GROUP BY user_id
            '''
        )
        return points['sum']