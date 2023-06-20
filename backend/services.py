import fastapi as _fastapi
import datetime as _dt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
from loguru import logger

import database as _database
import models as _models
import schemas as _schemas


def use_definition():
    return _database.Base.metadata.create_all(bind=_database.engine)
