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

    def visited(self, user, event):
        self.engine.execute(
            text('''
            INSERT INTO user_visited_event(user_id, event_id) 
            VALUES(:user_id, :event_id)
            '''),
            user_id = user.id, event_id = event.id
        )

    def checkCode(self, code):
        result = self.engine.execute(
            text('''
            SELECT id, name, code, amount, dt, description FROM event
            WHERE code LIKE :code AND NOW() <= (dt::timestamp + '1 day'::interval) AND NOW() >= dt
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
            SELECT id, name, code, amount, dt, description FROM event
            WHERE dt >= NOW()
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
        