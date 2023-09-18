
from spiderSystem.request import Request
class BaseSpider(object):

    name = 'demo'
    def start_requests(self):
        """生成器"""
        yield Request("http://www.example.com",name=self.name)
    def parse(self, response):
        """生成器"""
        yield

    def data_clean(self, data):
        return data

    def data_save(self, data):
        pass
