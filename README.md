# 持久化队列
1. scrapy - queuelib 队列 （硬盘中 disk_queue），基于
    1. 有基于文件 sqlite 的 持久化
2. pyspider - redis_queue 模块
    1. 基于 redis 的队列
        1. fifo队列 用 lists 列表，lpush,rpop
        2. lifo队列 用 lists 列表，lpush，lpop
        3. 优先级队列，用 Sorted Set 有序集合，zadd ，zrang ，zrem

```python
from request_manager.utils.redis_tools import get_redis_queue_cls

Queue = get_redis_queue_cls('priority')
PRIORITY_REDIS_QUEUE_CONFIG = {
    "name":"pqueue",
    "use_lock":True,  # 锁
    "redis_lock_config":{
        "lock_name": "pqueue-lock"
    }
}

pqueue = Queue(**PRIORITY_REDIS_QUEUE_CONFIG)
pqueue.put((100, 'value100'))
print(pqueue.get())
```
# 锁
1. 因为 优先级队列 priority，是基于 redis 中的有序集合来实现的，要弹出某个值，是需要 zrange，和 zrem，两条命令中有时间差，所有加锁比较好

### 在优先级队列实现加锁
1. 在取值方法中，先获取锁 self.lock.acquire_lock()
2. 再进行一些列操作后，再释放锁 self.lock.release_lock()
```python
  def get_nowait(self):
        """
        -1,-1默认取权重最大的
        0，,0 取权重最小的
        :return:
        """
        if self.use_lock is True:
            from .redis_lock import RedisLock
            if self.lock is None:
                self.lock = RedisLock(**self.redis_lock_config)

            if self.lock.acquire_lock():
                ret = self.redis.zrange(self.name, -1, -1)
                if not ret:
                    raise self.Empty
                self.redis.zrem(self.name, ret[0])
                self.lock.release_lock()
                return pickle.loads(ret[0])
        else:
            ret = self.redis.zrange(self.name, -1, -1)
            if not ret:
                raise self.Empty
            self.redis.zrem(self.name, ret[0])
            return pickle.loads(ret[0])
```
3. 锁本身的实现
- 基于 redis 中的用setnx设置某个值，（顺带加上过期时间，防止死锁，具体时间按照自己的业务逻辑来定合理的值）
- 如果能设置，说明没锁；不能设置，说明已经上锁
- 如果用户传了 block = True 参数，说明要阻塞，用一个 while 循环
```python
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

```
```python
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
```
- 执行 request_manager/utils/redis_tools/redis_lock.py
```python
# 测试
if __name__ == '__main__':
    redis_lock = RedisLock('redis_lock')

    if redis_lock.acquire_lock(expire=2):
        print('执行对应的操作')
        # redis_lock.release_lock()  # 加锁后不解锁试试
```
