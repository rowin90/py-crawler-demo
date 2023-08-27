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


from redis_queue.priority_redis_queue import PriorityRedisQueue

q = PriorityRedisQueue('pqueue')
q.put((100, 'value100'))

r1 = q.get(block=False)
print(r1)
