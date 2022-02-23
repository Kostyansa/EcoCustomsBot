import logging
from sqlalchemy.engine import Engine

from entity.user import User, Role
from sqlalchemy.sql import text

class UserRepository:
    def __init__(self, engine : Engine) -> None:
        self.engine = engine

    def get(self, user : User):
        user = self.engine.execute(
        text('''
        SELECT id as id, telegram_id as telegram_id, role as role
        FROM public.user 
        WHERE user.id = :id
        '''),
        id = user.id
        ).fetchone()
        if user is not None:
            return User(user['id'], user['telegram_id'], role = Role(user['role']))
        else:
            return None

    def elevate_user(self, user: User):
        self.engine.execute(
        text('''
        UPDATE public.user 
        SET role = :role
        WHERE id = :id
        '''),
        id = user.id,
        role = Role.ADMIN.value
        )

    def save(self, user : User):
        self.engine.execute(text('''
        INSERT INTO public.user(telegram_id, role) VALUES
        (:telegram_id, :role)
        '''),
        telegram_id = user.telegram_id,
        role = user.role.value
        )

    def get_from_telegram(self, telegram_id : str):
        user = self.engine.execute(
        text('''
        SELECT id as id, telegram_id as telegram_id, role as role
        FROM public.user 
        WHERE telegram_id = :telegram_id
        '''),
        telegram_id = telegram_id
        ).fetchone()
        if user is not None:
            return User(user['id'], user['telegram_id'], role = Role(user['role']))
        else:
            return None

    

    