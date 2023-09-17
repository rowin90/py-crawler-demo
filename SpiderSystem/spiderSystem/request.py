# 构建请求对象
import urllib.parse

class Request(object):
    def __init__(self, url, method='GET', query={}, body={},name="request",headers=None):
        self.url = url
        self.method = method

        if not isinstance(query, dict):
            raise Exception('query must be a dict')
        self.query = query

        if not isinstance(query, dict):
            raise Exception('body must be a dict')
        self.body = body
        self.headers = headers

        self.name = name # 当前请求属于哪个爬虫

    @property
    def url_with_query(self):
        """
        把字典的请求参数与url地址里的请求参数进行整合
        """
        url = self.url
        _ = urllib.parse.urlparse(url)
        url_without_query = _.scheme + '://' + _.hostname + _.path

        url_query = urllib.parse.parse_qsl(_.query)

        query = self.query.items()
        all_query = sorted(set(list(query) + url_query))

        return url_without_query + "?" + urllib.parse.urlencode(all_query)
