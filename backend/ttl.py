import threading as _threading
import datetime as _dt

from loguru import logger as _logger

import services as _services
import database as _database
import models as _models
import schemas as _schemas


"""
Модуль, контролирующий удаление устаревших данных.
Должен быть запущен в отдельном процессе

"""

_logger.add("./logs/debug.log")


class TtlController():

    frequency: int
    timer: _threading.Timer

    def __init__(self, frequency: int = 3600):
        self.frequency = frequency
        _logger.debug("TtlController started")
        self.set_timer()

    def set_timer(self):
        self.timer = _threading.Timer(self.frequency, self.check)
        self.timer.start()

    def check(self):
        _logger.debug("started checking")
        try:
            self.check_expired_links()
            self.check_unverified_emails()
        except Exception as e:
            _logger.error(f"check stopped with error: {e}")
        else:
            _logger.debug("finished checking successfuly")
        finally:
            self.set_timer()

    def check_unverified_emails(self):
        try:
            se = _database.SessionLocal()
            now = _dt.datetime.now().timestamp()
            for user in se.query(_models.User).filter_by(confirmed=False):
                schema = _schemas.SqlUser.from_orm(user)
                if now - schema.date_created.timestamp() > 3600:
                    se.delete(user)
                    se.commit()
                    _logger.debug(f"user {schema.id} deleted: mail not verified for a long time")
        finally:
            se.close()

    def check_expired_links(self):
        try:
            se = _database.SessionLocal()
            now = _dt.datetime.now()
            for link in se.query(_models.Link):
                schema = _schemas.Link.from_orm(link)
                if schema.limit == schema.count_used:
                    se.delete(link)
                    se.commit()
                    _logger.debug(f"link {schema.id} deleted: usage threshold exceeded")
                elif schema.date_expired and schema.date_expired < now:
                    se.delete(link)
                    se.commit()
                    _logger.debug(f"link {schema.id} deleted: date expired")
        finally:
            se.close()


if __name__ == "__main__":
    TtlController()
