from sqlalchemy.engine import Engine

from entity.user import User

class UserRepository:
    def __init__(self, engine : Engine) -> None:
        self.engine = engine

    def get(self, user : User):
        user = self.engine.execute(
        '''
        SELECT user.id, user.telegram_id, role.name
        FROM user 
        LEFT JOIN user_has_role on user.id = user_has_role.user_id 
        LEFT JOIN role on user_has_role.role_id = role.id
        WHERE user.id = :id
        ''',
        id = user.id
        )

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
        SELECT user.id, user.telegram_id, role.name
        FROM user 
        LEFT JOIN user_has_role on user.id = user_has_role.user_id 
        LEFT JOIN role on user_has_role.role_id = role.id
        WHERE user.telegram_id = :telegram_id
        ''',
        telegram_id = telegram_id
        )

    

    