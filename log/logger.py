# 将日志在控制台显示的同时写入log文件
# shatong
# 2019-12-18 17：25：06

import logging
import os
import time


class Logger:
    def __init__(self, name=__name__):
        # 创建一个loggger
        self.__name = name
        self.logger = logging.getLogger(self.__name)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        log_path = os.path.dirname(os.path.abspath(__file__))  # 取得系统目录
        log_path = log_path + '/log/'
        isExists = os.path.exists(log_path)
        # 判断结果
        if not isExists:
            os.makedirs(log_path)
            print(log_path + ' 创建成功')
        logname = log_path + 'debug_' + time.strftime('%Y-%m-%d') + '.log'  # 以日期为单位输出的日志文件名，防止日志文件过大
        fh = logging.FileHandler(logname, mode='a', encoding='utf-8')  # 不拆分日志文件，a指追加模式,w为覆盖模式
        fh.setLevel(logging.DEBUG)

        # 创建一个handler，用于将日志输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s-%(filename)s-[line:%(lineno)d]'
                                      '-%(levelname)s-[日志信息]: %(message)s',
                                      datefmt='%a, %d %b %Y %H:%M:%S')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    @property
    def get_log(self):
        """定义一个函数，回调logger实例"""
        return self.logger


log = Logger(__name__).get_log
# log.error('模块直接执行打印日志')
# log.debug('模块直接执行打印日志')
# log.info('模块直接执行打印日志')