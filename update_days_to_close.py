import os
import pytz
from datetime   import datetime

from sqlalchemy import (
    create_engine, Column, Integer, String, Date, DateTime, Boolean, ForeignKey
)
from sqlalchemy.orm             import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema      import ForeignKey

DB_HOST       = os.environ.get('DB_HOST')
DB_PORT       = os.environ.get('DB_PORT')
DB_USER       = os.environ.get('DB_USER')
DB_PASSWORD   = os.environ.get('DB_PASSWORD')
DB_ENGINE_URL = f'mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/letterlog'

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

def main():
    engine  = create_engine(DB_ENGINE_URL, encoding='utf-8')
    Session = sessionmaker(bind=engine)
    session = Session()

    timezone = pytz.timezone('Asia/Seoul')
    now      = datetime.now(timezone).date()
    
    postboxes = session.query(Postbox)
    updated_postboxes = [
        {
            'id': postbox.id,
            'days_to_close': (postbox.closed_at - now).days
        } for postbox in postboxes
    ]
    session.bulk_update_mappings(Postbox, updated_postboxes)
    session.commit()

if __name__ == '__main__':
    main()
