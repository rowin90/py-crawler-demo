# 持久化队列
```python
from redis_tools import get_redis_queue_cls

Queue = get_redis_queue_cls('priority')
PRIORITY_REDIS_QUEUE_CONFIG = {
    "name":"pqueue",
    "use_lock":True,
    "redis_lock_config":{
        "lock_name": "pqueue-lock"
    }
}

pqueue = Queue(**PRIORITY_REDIS_QUEUE_CONFIG)
pqueue.put((100, 'value100'))
print(pqueue.get())
```
