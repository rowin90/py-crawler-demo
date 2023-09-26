import logging
import time


def set_logging_config(format, datefmt, filename, filemode="a", level=logging.DEBUG):

    # 设置基本的日志为文件日志输出
    logging.basicConfig(
        level=level,
        format=format,
        datefmt=datefmt,
        filename=filename,
        filemode=filemode
    )

    # 添加终端日志输出
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(format)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


# 使用
if __name__ == '__main__':
    format =  '%(asctime)s  [process: %(process)d:][thread: %(thread)d] %(levelname)s  %(filename)s [line:%(lineno)d] %(levelname)s %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    filename = './spider.log'
    set_logging_config(format,datefmt,filename)

    while True:
        time.sleep(1)
        logging.debug('hello')
        logging.info('info')
        logging.warning('warning')
