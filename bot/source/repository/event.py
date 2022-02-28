import logging
from sqlalchemy.engine import Engine

from entity.event import Event
from sqlalchemy.sql import text

class EventRepository:
    def __init__(self, engine : Engine) -> None:
        self.engine = engine

    def add(self, event : Event):
        self.engine.execute(
            text('''
            INSERT INTO event(name, code, amount, dt, description)
            VALUES(:name, :code, :amount, :dt, :description)
            '''),
            name = event.name,
            code = event.code,
            amount = event.points,
            dt = event.date,
            description = event.description
        )

    def remove(self, event : Event):
        self.engine.execute(
            text('''
            DELETE from event
            WHERE id = :id
            '''),
            id = event.id
        )

    def visited(self, user, event):
        self.engine.execute(
            text('''
            INSERT INTO user_visited_event(user_id, event_id) 
            VALUES(:user_id, :event_id)
            '''),
            user_id = user.id, event_id = event.id
        )


    def checkVisited(self, user, event):
        result = self.engine.execute(
            text('''
            SELECT event_id from user_visited_event
            where user_id = :user_id and event_id = :event_id
            '''),
            user_id = user.id, event_id = event.id
        ).fetchone()
        if result is not None:
            return True
        else:
            return False

    def checkCode(self, code):
        result = self.engine.execute(
            text('''
            SET TIMEZONE='posix/Europe/Samara';
            SELECT id, name, code, amount, dt, description FROM event
            WHERE (code = :code) AND (NOW() >= dt) AND ((NOW() - '1 day'::interval) <= dt)
            '''),
            code = code
        ).fetchone()
        if result is not None:
            return Event(result['id'], result['name'], result['code'], result['amount'], result['dt'], result['description'])
        else:
            return None

    def getAll(self):
        result = self.engine.execute(
            text('''
            SET TIMEZONE='posix/Europe/Samara';
            SELECT id, name, code, amount, dt, description FROM event
            WHERE dt >= (NOW() - '1 day'::interval)
            ORDER BY dt
            ''')
        ).fetchall()
        events = [] 
        logging.info(result)
        for row in result:
            events.append(Event(row['id'], row['name'], row['code'], row['amount'], row['dt'], row['description']))
        return events

    
    def get(self, id):
        result = self.engine.execute(
            text('''
            SELECT id, name, code, amount, dt, description FROM event
            WHERE id = :id
            '''),
            id = id
        ).fetchone()
        if result is not None:
            return Event(result['id'], result['name'], result['code'], result['amount'], result['dt'], result['description'])
        else:
            return None
        