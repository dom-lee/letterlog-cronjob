import smtplib

class EmailServer:
    def __init__(self, GMAIL_USER, GMAIL_PASSWORD, url='smtp.gmail.com', port=465):
        self.url            = url
        self.port           = port
        self.GMAIL_USER     = GMAIL_USER
        self.GMAIL_PASSWORD = GMAIL_PASSWORD

    def login(self):
        try:
            email_server = smtplib.SMTP_SSL(self.url, self.port)
            email_server.ehlo()
            email_server.login(self.GMAIL_USER, self.GMAIL_PASSWORD)

            return email_server
        except:
            raise Exception('Email Server Error')