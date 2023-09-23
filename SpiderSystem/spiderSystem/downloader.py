import requests

from tornado.httpclient import HTTPClient, HTTPRequest, AsyncHTTPClient

from spiderSystem.response import Response


class RequestsDownloader(object):
    """根据request发起请求，构建response对象"""

    def fetch(self, request):
        if request.method.upper() == "GET":
            resp = requests.get(request.with_query_url, headers=request.headers)
        elif request.method.upper() == "POST":
            resp = requests.post(request.with_query_url, headers=request.headers, body=request.body)
        else:
            raise Exception('only support GET or POST Method')

        return Response(request, status_code=resp.status_code, url=resp.url, headers=resp.headers, body=resp.content)


class TornadoDownloader(object):

    def __init__(self):
        self.httpclient = HTTPClient()

    def fetch(self, request):
        print("tornado 同步客户端发的请求")
        tornado_request = HTTPRequest(request.with_query_url, method=request.method.upper(), headers=request.headers)
        tornado_response = self.httpclient.fetch(tornado_request)
        return Response(request=request, status_code=tornado_response.code, url=tornado_response.effective_url,
                        body=tornado_response.buffer.read())

    """
    同步的请求，不能复用，需要用完后关闭
    """

    def __del__(self):
        self.httpclient.close()


class AsyncTornadoDownloader(object):

    def __init__(self):
        self.async_http_client = AsyncHTTPClient()

    async def fetch(self, request):
        print("tornado 异步客户端发的请求")
        tornado_request = HTTPRequest(request.with_query_url, method=request.method.upper(), headers=request.headers)
        tornado_response = await self.async_http_client.fetch(tornado_request)
        return Response(request=request, status_code=tornado_response.code, url=tornado_response.effective_url,
                        headers=request.headers,
                        body=tornado_response.buffer.read())
