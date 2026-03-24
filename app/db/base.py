from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from models import user
from models import jwt_token_blacklist