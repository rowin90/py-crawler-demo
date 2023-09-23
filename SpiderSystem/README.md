# Master 和 Slave
1. master 是用来处理请求，过滤的
2. slave 是用来下载，转化的

# 启动
1. 启动 master 进程，自己编写 usage.py, 在里面写脚本启动
2. 注释掉 Slave，执行就是Master;相反就是启动 Slave
```python

if __name__ == '__main__':
    spiders = {BaiduSpider.name: BaiduSpider}
    Master(spiders, project_name=PROJECT_NAME, request_manager_config=REQUEST_MANAGER_CONFIG).run()

    # 同步请求，用 requests 发请求
    # Slave(spiders, project_name=PROJECT_NAME, request_manager_config=REQUEST_MANAGER_CONFIG).run()

    # slave = Slave(spiders, project_name=PROJECT_NAME, request_manager_config=REQUEST_MANAGER_CONFIG)
    # io_loop = tornado.ioloop.IOLoop.current()
    # io_loop.run_sync(slave.run)

```
