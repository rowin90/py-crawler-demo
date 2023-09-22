from .request_manager import RequestManager
from .request_manager.utils.redis_tools import get_redis_queue_cls
from .downloader import RequestsDownloader

from .request import Request

REQUEST_MANAGER_CONFIG = {
    "queue_type": "fifo",
    "queue_kwargs": {"host": "localhost", "port": 6379},
    "filter_type": "redis",  # 过滤器类型，基于redis的过滤器
    "filter_kwargs": {"redis_key": "redis_filter", "redis_host": "localhost"}
}

PROJECT_NAME = 'baidu'
FIFO_QUEUE = get_redis_queue_cls('fifo')


class Master(object):

    def __init__(self, spiders):
        self.filter_queue = FIFO_QUEUE("filter_queue", host="localhost")  # 请求过滤队列
        self.request_manager = RequestManager(**REQUEST_MANAGER_CONFIG)  # 请求管理对象
        self.spiders = spiders

    def run_start_requests(self):
        for spider in self.spiders.values():
            for request in spider().start_requests():
                self.filter_queue.put(request)

    def run_filter_queue(self):
        while True:
            request = self.filter_queue.get()
            self.request_manager.add_request(request, PROJECT_NAME)

    def run(self):
        self.run_start_requests()
        self.run_filter_queue()


class Slave(object):
    def __init__(self, spiders):
        self.filter_queue = FIFO_QUEUE("filter_queue", host="localhost")
        self.request_manager = RequestManager(**REQUEST_MANAGER_CONFIG)  # 请求管理对象
        self.downloader = RequestsDownloader()
        self.spiders = spiders

    def run(self):
        while True:
            # 1. 获取一个请求
            request = self.request_manager.get_request(PROJECT_NAME)

            # 2. 发起请求
            response = self.downloader.fetch(request)

            # 3. 获取爬虫对象
            spider = self.spiders[request.name]()

            # 4. 处理 response
            for result in spider.parse(response):
                if result is None:
                    raise Exception('不允许返回None')
                elif isinstance(result, Request):
                    self.filter_queue.put(result)
                else:
                    # 意味着是一个数据
                    new_result = spider.data_clean(result)
                    spider.data_save(new_result)
