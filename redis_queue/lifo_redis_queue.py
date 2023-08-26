import pickle
from .base import BaseRedisQueue


class LifoRedisQueue(BaseRedisQueue):
    def get_nowait(self):
        ret = self.redis.rpop(self.name)
        if ret is None:
            raise self.Empty
        return pickle.loads(ret)
