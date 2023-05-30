import json
from django.conf import settings
import redis


# Connect to the Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)

def createFeed(post_list, user_id):
    # Set the list of posts in Redis.
    redis_instance.set(user_id, json.dumps(post_list))


def readFeed(user_id):
    # Get the list of posts from Redis.
    feed_object_as_bytes = redis_instance.get(user_id)
    # print("In readFeed:", type(feed_object_as_bytes)) # bytes
    feed_obj_as_dict = json.loads(feed_object_as_bytes.decode("utf-8"))

    post_list = feed_obj_as_dict

    # Return the list of posts.
    return post_list
