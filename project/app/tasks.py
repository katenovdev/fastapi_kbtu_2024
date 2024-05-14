import dramatiq

from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends.redis import RedisBackend
from app.email import send_password_email 

REDIS_URL = "redis://:123456@localhost:6379/0"

redis_broker = RedisBroker(url=REDIS_URL)
result_backend = RedisBackend(url=REDIS_URL)
redis_broker.add_middleware(Results(backend=result_backend))

dramatiq.set_broker(redis_broker)

@dramatiq.actor()
def generate_and_send_password_email(email, password):
        send_password_email("mail@gmail.com", "password", email, password )
        