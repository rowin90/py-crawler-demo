import requests

from spiderSystem.response import Response

class RequestsDownloader(object):
    """根据request发起请求，构建response对象"""
    def fetch(self,request):
        if request.method.upper() == "GET":
            resp = request.get(request.with_query_url,headers=request.headers)
        elif request.method.upper() == "POST":
            resp = request.posy(request.with_query_url,headers=request.headers,body=request.body)
        else:
            raise Exception('only support GET or POST Method')

        return Response(request, status_code=resp.status_code, url=resp.url, headers=resp.headers, body=resp.content)
