import pytz
from datetime   import datetime

from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Boolean, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema      import ForeignKey

from settings   import DB_ENGINE_URL

Base = declarative_base()

class Postbox(Base):
    __tablename__ = 'postboxes'

    id            = Column(Integer, primary_key=True)
    uuid          = Column(String(32))
    name          = Column(String(100))
    password      = Column(String(100))
    is_public     = Column(Boolean)
    send_at       = Column(Date)
    closed_at     = Column(Date)
    days_to_close = Column(Integer)
    created_at    = Column(DateTime)

    @classmethod
    def get_postboxes_to_send(cls, database):
        timezone = pytz.timezone('Asia/Seoul')
        today    = datetime.now(timezone).date()

        query = '''SELECT * FROM postboxes WHERE send_at=%s'''
        return database.execute(query, (today))

class Receiver(Base):
    __tablename__ = 'receivers'

    id         = Column(Integer, primary_key=True)
    email      = Column(String(200))
    created_at = Column(DateTime)
    postbox_id = Column(Integer, ForeignKey('postboxes.id'))