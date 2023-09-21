import re

import lxml.etree
from bs4 import BeautifulSoup
from pyquery import PyQuery


class Response(object):
    """响应对象"""

    def __init__(self, request, status_code, url, headers, body):
        self.request = request
        self.status_code = status_code
        self.url = url
        self.headers = headers
        self.body = body

    def xpath(self, rule):
        html = lxml.etree.HTML(self.body)
        return html.xpath(rule)

    def select(self, rule):
        soup = BeautifulSoup(self.body, 'lxml')
        return soup.select(rule)

    def d(self, rule):
        d = PyQuery(lxml.etree.HTML(self.body))
        return d(rule)

    def re_math(self, rule):
        return re.match(rule, self.body)

    def re_search(self, rule):
        return re.search(rule, self.body)

    def re_findall(self, rule):
        return re.findall(rule, self.body)
