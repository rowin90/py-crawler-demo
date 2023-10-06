import requests
import sys
class P:
    name = 1

    @staticmethod
    def getName():
        return 222

    @property
    def getAge(self):
        return 333


a = P()

print(a.name)
print(a.getName())
print(a.getAge)
print('=============')
print('=============')
print(P.getName())
print(P.getAge)
print(sys.platform)
print(requests.get('http://www.baidu.com'))
