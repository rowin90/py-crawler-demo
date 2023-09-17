def get_redis_queue_cls(queue_type):
    if queue_type == 'fifo':
        from .fifo_redis_queue import FifoRedisQueue
        return FifoRedisQueue
    elif queue_type == 'lifo':
        from .lifo_redis_queue import LifoRedisQueue
        return LifoRedisQueue
    elif queue_type == 'priority':
        from .priority_redis_queue import PriorityRedisQueue
        return PriorityRedisQueue
    else:
        raise Exception('只支持 fifo,lifo,priority三种队列类型')


def get_redis_lock_cls():
    from .redis_lock import RedisLock
    return RedisLock
