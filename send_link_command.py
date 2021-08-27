from email.mime.text import MIMEText

from sqlalchemy import create_engine

from models         import Postbox
from email_server   import EmailServer
from settings       import DB_ENGINE_URL, GMAIL_USER, GMAIL_PASSWORD, get_logger

def main():
    email_server = EmailServer(GMAIL_USER, GMAIL_PASSWORD)
    email_server = email_server.login()

    with create_engine(DB_ENGINE_URL).connect() as conn:
        postboxes = Postbox.get_postboxes_to_send(conn)

        for postbox in postboxes:
            collection_link_url = f'letterlog.me/collections/{postbox.uuid}'
            msg = MIMEText(collection_link_url)
            msg['Subject'] = 'Letterlog로 부터 온 추억입니다.'

            query = '''
                SELECT `email` FROM `receivers`
                WHERE `postbox_id` = %s
            '''
            receivers = conn.execute(query, (postbox.id))
            receivers_email = [receiver[0] for receiver in receivers]

            email_server.sendmail(GMAIL_USER, receivers_email, msg.as_string())

if __name__ == '__main__':
    main()

    logger = get_logger('send_link_command')
    logger.debug('Send Link')