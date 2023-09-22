import logging
from spiderSystem.request_manager.utils.redis_tools import get_redis_queue_cls
class RequestManager(object):

    def __init__(self,
                queue_type="fifo",
                filter_type="redis",
                queue_kwargs={},
                filter_kwargs={}
                ):
        self._queue = {}
        self._filters = {}

        self._filter_kwargs = filter_kwargs  # 实例化过滤器
        self._queue_kwargs = queue_kwargs  # 实例化队列对象的关键词

        self._set_filter_cls(filter_type)
        self._set_queue_cls(queue_type)


    def _set_filter_cls(self, filter_type):
        pass

    def _set_queue_cls(self, queue_type):
        """设置请求队列使用的 类对象"""
        FIFO_QUEUE = get_redis_queue_cls(queue_type)
        self.filter_queue = FIFO_QUEUE("filter_manager_queue", host="localhost")

    def _get_request_filter(self, filter_name):
        pass

    def _get_request_queue(self, queue_name):
        pass

    def add_request(self, request_obj, queue_name, filter_name=None):
        """对请求去重，并将非重复的请求对象添加到指定请求队列中"""
        request = request_obj
        self.filter_queue.put(request)

        print(request)
        print('请求添加成功: <%s>' % request.url)
        pass

    def get_request(self, queue_name, block=True):
        """从指定队列中获取请求对象"""
        request = self.filter_queue.get(block=True)
        return request
