import tornado.ioloop
from spiderSystem.main import Master, Slave
from spiderSystem.request import Request
from spiderSystem.spider import BaseSpider

REQUEST_MANAGER_CONFIG = {
    "queue_type": "fifo",
    "queue_kwargs": {"host": "localhost", "port": 6379},
    "filter_type": "redis",  # 过滤器类型，基于redis的过滤器
    "filter_kwargs": {"redis_key": "redis_filter", "redis_host": "localhost"}
}

PROJECT_NAME = 'baidu'


class BaiduSpider(BaseSpider):
    name = 'baidu'

    def start_requests(self):
        """生成器"""
        yield Request("http://www.baidu.com/s?wd=python", name=self.name)
        yield Request("http://www.baidu.com/s?wd=python1", name=self.name)
        yield Request("http://www.baidu.com/s?wd=python2", name=self.name)
        yield Request("http://www.baidu.com/s?wd=python3", name=self.name)
        yield Request("http://www.baidu.com/s?wd=python4", name=self.name)
        yield Request("http://www.baidu.com/s?wd=python5", name=self.name)

    def parse(self, response):
        """生成器"""
        print(response)
        print(response.url)
        yield response.body

    def data_clean(self, data):
        return data

    def data_save(self, data):
        pass


if __name__ == '__main__':
    spiders = {BaiduSpider.name: BaiduSpider}
    # Master(spiders, project_name=PROJECT_NAME, request_manager_config=REQUEST_MANAGER_CONFIG).run()

    # 同步请求，用 requests 发请求
    # # Slave(spiders, project_name=PROJECT_NAME, request_manager_config=REQUEST_MANAGER_CONFIG).run()
    #
    slave = Slave(spiders, project_name=PROJECT_NAME, request_manager_config=REQUEST_MANAGER_CONFIG)
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.run_sync(slave.run)
