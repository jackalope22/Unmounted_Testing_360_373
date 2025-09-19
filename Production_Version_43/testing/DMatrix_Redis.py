import redis

redis_client = redis.Redis(host="172.27.2.72", port=6379)

def getRedisClient():
    return redis_client