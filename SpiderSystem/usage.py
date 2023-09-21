from spiderSystem.main import Master, Slave
from spiderSystem.request import Request
from spiderSystem.spider import BaseSpider


class BaiduSpider(BaseSpider):
    name = 'baidu'

    def start_requests(self):
        """生成器"""
        yield Request("http://www.baidu.com/1", name=self.name)
        yield Request("http://www.baidu.com/2", name=self.name)
        yield Request("http://www.baidu.com/3", name=self.name)
        yield Request("http://www.baidu.com/4", name=self.name)
        yield Request("http://www.baidu.com/5", name=self.name)

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
    # Master(spiders).run()
    Slave(spiders).run()
