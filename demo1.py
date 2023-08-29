"""
调度模块整体demo
"""
from six.moves import queue

from request_manager.request import Request
from request_manager import RequestScheduler

REQUEST_SCHEDULER_CONFIG = {
    "queue_type": "fifo",
    "queue_kwargs": {"host": "localhost", "port": 6379},
    "filter_type": "redis",
    "filter_kwargs": {"redis_key": "redis_filter", "redis_host": "localhost"}
}

request_scheduler = RequestScheduler(**REQUEST_SCHEDULER_CONFIG)

baidu_url = "https:/www.baidu.com/s?wd="

request_objs = [
    Request(baidu_url + '1', name="baidu"),
    Request(baidu_url + '1', name="baidu"),
    Request(baidu_url + '2', name="baidu"),
    Request(baidu_url + '3', name="baidu"),
    Request(baidu_url + '3', name="baidu"),
    Request(baidu_url + '4', name="baidu"),
]

def add_requests(objs):
    for r in objs:
        request_scheduler.add_request(r,r.name)

def get_requests(queue_name):
    while True:
        try:
            request = request_scheduler.get_request(queue_name,block=True)
        except queue.Empty:
            break
        else:
            yield request

add_requests(request_objs)
