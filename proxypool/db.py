import redis
from .setting import HOST,PORT,PASSWORD

class RedisClient(object):
    def __init__(self):
        if PASSWORD:
            self._db = redis.Redis(host=HOST,port=PORT,password=PASSWORD)
        else:
            self._db = redis.Redis(host=HOST,port=PORT)

    def get(self,count = 1):
        # 从代理最左侧拿出一个代理
        pxoxy = self._db.lrange("proxies",count-1,0)
        # 删除最左侧的代理
        self._db.ltrim("proxies",count,-1)
        return pxoxy

    def put(self,proxy):
        # 将代理放到代理队列的最右测
        self._db.rpush("proxies",proxy)


    def pop(self):
        # 从右边获取一个代理并将其删除
        proxy = self._db.lpop("proxies").decode('utf-8')
        return proxy

    @property
    def queue_len(self):
        #获取代理的长度
        return self._db.llen("proxies")

    def flush(self):
        #清空数据库
        return self._db.flushall()



if __name__ == '__mian__':
    coon = RedisClient()
    print(coon.pop())

