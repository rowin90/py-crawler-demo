import time

import redis
import pickle


class RedisLock(object):
    def __init__(self, lock_name, host="localhost", port=6379, db=0):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        self.lock_name = lock_name

    def _get_thread_id(self):
        import threading
        import socket
        import os
        # thread_id = "服务器号" + "进程号" +  threading.currentThread().name
        thread_id = socket.gethostname() + str(os.getpid()) + threading.currentThread().name
        return thread_id

    def acquire_lock(self, thread_id=None, expire=10 ,block = True):

        if thread_id is None:
            thread_id = self._get_thread_id()


        while block:
            # 如果 lock_name 存在，ret == 0 否则 ret==1
            ret = self.redis.setnx(self.lock_name, pickle.dumps(thread_id))
            if ret == 1:
                self.redis.expire(self.lock_name, expire)
                print('上锁成功')
                return True
            time.sleep(0.01)


        # 如果 lock_name 存在，ret == 0 否则 ret==1
        ret = self.redis.setnx(self.lock_name, pickle.dumps(thread_id))
        if ret == 1:
            self.redis.expire(self.lock_name, expire)
            print('上锁成功')
            return True
        else:
            print('上锁失败')
            return True


    def release_lock(self, thread_id=None):
        if thread_id is None:
            thread_id = self._get_thread_id()

        ret = self.redis.get(self.lock_name)

        if ret is not None and pickle.loads(ret) == thread_id:
            self.redis.delete(self.lock_name)
            print('解锁成功')
            return True
        else:
            print('解锁失败')
            return False


if __name__ == '__main__':
    redis_lock = RedisLock('redis_lock')

    if redis_lock.acquire_lock(expire=2):
        print('执行对应的操作')
        # redis_lock.release_lock()  # 加锁后不解锁试试
