from sqlalchemy.engine import Engine

class ResponseRepository:
    def __init__(self, engine : Engine) -> None:
        self.engine = engine

    

    