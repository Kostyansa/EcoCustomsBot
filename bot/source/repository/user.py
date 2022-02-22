from sqlalchemy.engine import Engine

from entity.user import User, Role

class UserRepository:
    def __init__(self, engine : Engine) -> None:
        self.engine = engine

    def get(self, user : User):
        user = self.engine.execute(
        '''
        SELECT id as id, telegram_id as telegram_id, role as role
        FROM user 
        WHERE user.id = :id
        ''',
        id = user.id
        ).fetchone()
        if user is not None:
            return User(user['id'], user['telegram_id'], Role(['role']))
        else:
            return None

    def save(self, user : User):
        self.engine.execute('''
        INSERT INTO user(telegram_id) VALUES
        (:telegram_id)
        ''',
        telegram_id = user.telegram_id,
        )

    def get_from_telegram(self, telegram_id : str):
        user = self.engine.execute(
        '''
        SELECT id as id, telegram_id as telegram_id, role as role
        FROM user 
        WHERE telegram_id = :telegram_id
        ''',
        telegram_id = telegram_id
        ).fetchone()
        if user is not None:
            return User(user['id'], user['telegram_id'], Role(['role']))
        else:
            return None

    

    