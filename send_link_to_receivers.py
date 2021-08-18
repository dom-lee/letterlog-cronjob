import os
import pytz
import smtplib
from datetime        import datetime
from email.mime.text import MIMEText

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

GMAIL_USER = os.environ.get('GMAIL_USER')
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')

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

class Receiver(Base):
    __tablename__ = 'receivers'

    id         = Column(Integer, primary_key=True)
    email      = Column(String(200))
    created_at = Column(DateTime)
    postbox_id = Column(Integer, ForeignKey('postboxes.id'))

def main():
    try:
        email_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        email_server.ehlo()
        email_server.login(GMAIL_USER, GMAIL_PASSWORD)
    except:
        raise Exception('Email Server Error')

    engine  = create_engine(DB_ENGINE_URL, encoding='utf-8')
    Session = sessionmaker(bind=engine)
    session = Session()

    timezone = pytz.timezone('Asia/Seoul')
    today    = datetime.now(timezone).date()
    
    postboxes = session.query(Postbox).filter(Postbox.send_at==today)

    for postbox in postboxes:
        collection_link_url = f'letterlog.me/collections/{postbox.uuid}'
        msg = MIMEText(collection_link_url)
        msg['Subject'] = 'Letterlog로 부터 온 추억입니다.'
        
        receivers = session.query(Receiver).filter(Receiver.postbox_id==postbox.id)
        receivers_email = [receiver.email for receiver in receivers]

        email_server.sendmail(GMAIL_USER, receivers_email, msg.as_string())

if __name__ == '__main__':
    main()
