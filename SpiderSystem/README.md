# 环境
1. 启动 redis。队列用的是 redis 队列

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

# 模块安装成内置环境中
1. 在模块目录添加 setup.py 脚本
```txt
├── setup.py
├── spiderSystem
├── README.md

```
2. 执行 pip3 setup.py install 即可
3. 查看包信息 pip3 show spiderSystem
```python
from setuptools import setup, find_packages

setup(
    name="spiderSystem",
    version="0.1",
    description="spiderSystem module",
    author='raoju',
    url="url",
    license="license",
    packages=find_packages(exclude=[]), # 当前所有模块都安装
    install_requires=[
        "tornado >= 5.1",
        "pycurl",
    ]

)

```
