from os import environ
from redis import Redis
from time import sleep
import random

def produce(data):
    with Redis( host="redis", port= "6379", db=0 ) as redis:
        redis.lpush( "buffer", data )
def consume():
    with Redis( host="redis", port= "6379", db=0 ) as redis:
        return redis.brpop("buffer")


print('Hello World!')
type = environ.get("TYPE", "CONSUMER")
print(type)
if type == "PRODUCER":
    while True:
        sleep( random.randint(1,5) )
        data = random.randint(1,100)
        produce(data)
        print(f"Produced {data}")

else:
    while True:
        sleep( random.randint(1,5) )
        data = consume()
        print(f"Consumed {data}")