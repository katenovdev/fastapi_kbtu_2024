import dramatiq

from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends.redis import RedisBackend
# from app.emails import send_password_email 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

REDIS_URL = "redis://:123456@localhost:6379/0"

redis_broker = RedisBroker(url=REDIS_URL)
result_backend = RedisBackend(url=REDIS_URL)
redis_broker.add_middleware(Results(backend=result_backend))

dramatiq.set_broker(redis_broker)

@dramatiq.actor()
def generate_and_send_password_email(email, password):
        send_password_email("somemail", "somepassword", email, password )

def send_password_email(sender_email, sender_password, recipient_email, password):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    server.login(sender_email, sender_password)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Ваш пароль'

    body = "Ваш пароль: {}".format(password)
    msg.attach(MIMEText(body, 'plain'))
    
    server.send_message(msg)

    server.quit()