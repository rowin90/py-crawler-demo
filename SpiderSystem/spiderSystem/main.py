import asyncio
import logging

import tornado.ioloop
import threading
import json

import redis

from .request_manager import RequestManager
from .request_manager.utils.redis_tools import get_redis_queue_cls
from .downloader import RequestsDownloader, TornadoDownloader, AsyncTornadoDownloader

from .request import Request

FIFO_QUEUE = get_redis_queue_cls('fifo')


class Master(object):

    def __init__(self, spiders, project_name, request_manager_config):
        self.filter_queue = FIFO_QUEUE("filter_queue", host="localhost")  # 请求过滤队列
        self.request_manager = RequestManager(**request_manager_config)  # 请求管理对象
        self.spiders = spiders
        self.project_name = project_name

    def run_start_requests(self):
        for spider in self.spiders.values():
            for request in spider().start_requests():
                self.filter_queue.put(request)

    def run_filter_queue(self):
        while True:
            request = self.filter_queue.get()
            self.request_manager.add_request(request, self.project_name)

    def run(self):
        # self.run_start_requests()
        # self.run_filter_queue()
        # 两个线程去做
        threading.Thread(target=self.run_start_requests).start()
        threading.Thread(target=self.run_filter_queue).start()


class RequestWatcher(object):
    def __init__(self):
        self.redis_client = redis.StrictRedis(host="localhost")

    def json_serializer(self, request, error=None):
        _ = {
            "url": request.url,
            "method": request.method,
            "query": request.query,
            "body": request.body,
            "name": request.name,
            "headers": request.headers,
            "id": request.id,
            "error": error
        }

        return json.dumps(_)

    def mark_process_requests(self, request):
        # 把请求对象添加到正在处理:字符串
        self.redis_client.hset("processing_requests", request.id, self.json_serializer(request))

    def unmark_process_requests(self, request):
        # 把请求对象添加到正在处理:字符串
        self.redis_client.hdel('processing_requests', request.id)

    def mark_fail_requests(self, request, error):
        # 标记失败
        self.redis_client.hset('fail_requests', request.id, self.json_serializer(request, error))


class Slave(object):
    def __init__(self, spiders, project_name, request_manager_config):
        self.filter_queue = FIFO_QUEUE("filter_queue", host="localhost")
        self.request_manager = RequestManager(**request_manager_config)  # 请求管理对象
        self.downloader = AsyncTornadoDownloader()
        self.spiders = spiders
        self.project_name = project_name

        self.request_watcher = RequestWatcher()

    async def handle_request(self):
        io_loop = tornado.ioloop.IOLoop.current()
        # 1. 获取一个请求
        future = io_loop.run_in_executor(None, self.request_manager.get_request, self.project_name)
        request = await future

        self.request_watcher.mark_process_requests(request)

        try:
            # 2. 发起请求
            response = await self.downloader.fetch(request)

            # 3. 获取爬虫对象
            spider = self.spiders[request.name]()

            # 4. 处理 response
            for result in spider.parse(response):
                if result is None:
                    raise Exception('不允许返回None')
                elif isinstance(result, Request):
                    await io_loop.run_in_executor(None, self.filter_queue.put, result)
                else:
                    # 意味着是一个数据
                    new_result = spider.data_clean(result)
                    spider.data_save(new_result)
        except Exception as e:
            logging.error(e)
            # 失败请求后
            self.request_watcher.mark_fail_requests(request, str(e))
            raise
        finally:
            # 成功请求后删除记录
            self.request_watcher.unmark_process_requests(request)

    async def run(self):
        while True:
            await asyncio.wait([
                self.handle_request(),
                self.handle_request(),
            ])
