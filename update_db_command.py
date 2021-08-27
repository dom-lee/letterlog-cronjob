import pytz
import logging
from datetime   import datetime

from sqlalchemy     import create_engine
from sqlalchemy.orm import Session

from models         import Postbox
from settings       import DB_ENGINE_URL, get_logger

def main():
    timezone = pytz.timezone('Asia/Seoul')
    now      = datetime.now(timezone).date()

    engine = create_engine(DB_ENGINE_URL)
    with Session(engine) as session:
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

    logger = get_logger('update_db_command')
    logger.debug('Update DB')