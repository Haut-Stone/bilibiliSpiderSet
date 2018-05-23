# -*- coding: utf-8 -*-
# @Author: Haut-Stone
# @Date:   2017-10-05 13:31:08
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2018-03-21 21:21:17


class Logger():
    '''
    命令行彩色终端
    '''
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

    # 无需实例化即可使用
    @staticmethod
    def ok(info):
        print(Logger.GREEN + info + Logger.ENDC)

    @staticmethod
    def warning(info):
        print(Logger.YELLOW + info + Logger.ENDC)

    @staticmethod
    def fail(info):
        print(Logger.RED + info + Logger.ENDC)
