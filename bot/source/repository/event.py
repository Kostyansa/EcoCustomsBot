from sqlalchemy.engine import Engine

from entity.event import Event

class EventRepository:
    def __init__(self, engine : Engine) -> None:
        self.engine = engine

    def add(self, event : Event):
        self.engine.execute(
            '''
            INSERT INTO event(name, code, amount, dt)
            VALUES(:name, :code, :amount, :dt)
            ''',
            name = event.name,
            code = event.code,
            amount = event.points,
            dt = event.date
        )

    def visited(self, user, event):
        self.engine.execute(
            '''
            INSERT INTO user_visited_event(user_id, event_id) 
            VALUES(:user_id, :event_id)
            ''',
            user_id = user.id, event_id = event.id
        )

    def checkCode(self, code):
        result = self.engine.execute(
            '''
            SELECT id, name, code, amount, dt FROM event
            WHERE code LIKE :code
            ''',
            code = code
        ).fetchone()
        if result is not None:
            return Event(result['id'], result['name'], result['code'], result['amount'], result['dt'])
        else:
            return None

    def getAll(self):
        result = self.engine.execute(
            '''
            SELECT id, name, code, amount, dt FROM event
            WHERE dt >= NOW()
            '''
        )
        rowcount = len(result._saved_cursor._result.rows)
        events = [] 
        for row in result:
            events.append(Event(row['id'], row['name'], row['code'], row['amount'], row['dt']))
        return events

    
    def get(self, id):
        result = self.engine.execute(
            '''
            SELECT id, name, code, amount, dt FROM event
            WHERE id = :id
            ''',
            id = id
        ).fetchone()
        if result is not None:
            return Event(result['id'], result['name'], result['code'], result['amount'], result['dt'])
        else:
            return None
        