# class Res():
#     def __init__(self):
#         self.age = 1
#
#
# a = Res()
# a.name = 3
# print(a.name)
import pickle

a = pickle.dumps('a')
print(a)
b = pickle.loads(a)
print(b)
