import redis
import pickle
class RedisLock(object):
    def __init__(self,lock_name,host="localhost",port=6379,db=0):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        self.lock_name = lock_name

    def acquire_lock(self,thread_id):

        # 如果 lock_name 存在，ret == 0 否则 ret==1
        ret = self.redis.setnx(self.lock_name,pickle.dumps(thread_id))

        if ret == 1:
            self.redis.expire(self.lock_name,2)
            print('上锁成功')
            return True
        else:
            print('上锁失败')
            return False
    def release_lock(self,thread_id):
        ret =  self.redis.get(self.lock_name)

        if ret is not None and pickle.loads(ret) == thread_id:
            self.redis.delete(self.lock_name)
            print('解锁成功')
            return True
        else:
            print('解锁失败')
            return False

if __name__ == '__main__':
    redis_lock = RedisLock('redis_lock')

    import threading
    thread_id = "服务器号" + "进程号" +  threading.currentThread().name

    if redis_lock.acquire_lock(thread_id):
        print('执行对应的操作')
        redis_lock.release_lock(thread_id)
