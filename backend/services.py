import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import datetime as _dt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
from loguru import logger

import database as _database
import models as _models
import schemas as _schemas
from config import JWT_SECRET


oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")


def use_definition():
    return _database.Base.metadata.create_all(bind=_database.engine)
