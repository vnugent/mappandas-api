from smtplib import SMTP, SMTPException
import os

sender = 'hola@mappandas.com'

message_template = ("""From: Viet Nguyen <hola@mappandas.com>
To: <{2}>
Subject: Your Panda 
Panda link:
https://app.mappandas.com/p/{0}

Description:
{1}

---
Ps: My name is Viet Nguyen and I'm the creator of Map Pandas.  """
           """If you have any questions about the app, please hit 'reply' and let me know.

This email was sent from hola@mappandas.com
""")

email_server = os.getenv('EMAIL_SERVER', 'localhost');
email_user = os.getenv('EMAIL_USER')
email_password = os.getenv('EMAIL_PASSWORD')


def preflight_check():
    if email_user is None:
        raise Exception("Missing EMAIL_USER env")

    if email_password is None:
        raise Exception("Missing EMAIL_PASSWORD env")
    try:
        SMTP(email_server, timeout=5).login(email_user, email_password,)
    except (OSError, SMTPException):
        raise RuntimeWarning("Can't connect to STMP server")


def sendmail(uuid, description, email):
    message = message_template.format(uuid, description, email)
    receivers = [email]

    try:
        with SMTP(email_server, timeout=5) as smtp:
            smtp.login(email_user, email_password)
            print(smtp.verify(receivers[0]))
            smtp.sendmail(sender, receivers, message)
            return 0
    except (OSError, SMTPException) as e1:
        print(e1)
        return 1
