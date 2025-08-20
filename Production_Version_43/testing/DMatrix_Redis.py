import redis

redis_client = redis.Redis(host="172.27.3.217", port=6379)

def getRedisClient():
    return redis_client