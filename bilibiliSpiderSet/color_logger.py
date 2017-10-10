# -*- coding: utf-8 -*-
# @Author: Haut-Stone
# @Date:   2017-10-05 13:31:08
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2017-10-05 20:50:45

class Logger():

	HEADER = '\033[95m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'

	@staticmethod
	def ok(info):

		print(Logger.GREEN + info + Logger.ENDC)

	@staticmethod
	def warning(info):

		print(Logger.YELLOW + info + Logger.ENDC)

	@staticmethod
	def fail(info):

		print(Logger.RED+ info + Logger.ENDC)