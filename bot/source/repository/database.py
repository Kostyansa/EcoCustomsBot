from sqlalchemy.engine import Engine
import logging

def init_database(engine):
    try:
        engine.execute(
            """
            CREATE TABLE IF NOT EXISTS user(
                id SERIAL,
                telegram_id TEXT UNIQUE NOT NULL,
                role INT,
                PRIMARY KEY (id)
            );

            CREATE TABLE IF NOT EXISTS user_points(
                id SERIAL,
                user_id INT NOT NULL,
                points INT NOT NULL,
                until DATETIME NOT NULL,
                PRIMARY KEY(id),
                FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS response(
                id SERIAL,
                message JSONB NOT NULL,
                PRIMARY KEY(id)
            );

            CREATE TABLE IF NOT EXISTS event(
                id SERIAL,
                name TEXT NOT NULL,
                code TEXT NOT NULL,
                amount INT NOT NULL,
                dt DATETIME NOT NULL,
                PRIMARY KEY(id)
            );

            CREATE TABLE IF NOT EXISTS user_visited_event(
                user_id INT NOT NULL,
                event_id INT NOT NULL,
                PRIMARY KEY(user_id, role_id),
                FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE,
                FOREIGN KEY(event_id) REFERENCES event(id) ON DELETE CASCADE
            );
            """
        )
    except Exception as exc:
        logging.warning("There was an error while initializing the database: %s", exc)
        raise Exception() from exc
    else:
        logging.debug("Database initialized successfully")