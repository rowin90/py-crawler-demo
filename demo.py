# class Res():
#     def __init__(self):
#         self.age = 1
#
#
# a = Res()
# a.name = 3
# print(a.name)


# import pickle
#
# a = pickle.dumps('a')
# print(a)
# b = pickle.loads(a)
# print(b)


from request_manager.utils.redis_tools import get_redis_queue_cls

Queue = get_redis_queue_cls('priority')
PRIORITY_REDIS_QUEUE_CONFIG = {
    "name": "pqueue",
    "use_lock": True,
    "redis_lock_config": {
        "lock_name": "pqueue-lock"
    }
}

pqueue = Queue(**PRIORITY_REDIS_QUEUE_CONFIG)
pqueue.put((100, 'value100'))
print(pqueue.get())

# r1 = q.get(block=False)
# print(r1)
