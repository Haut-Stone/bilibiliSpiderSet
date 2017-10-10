# -*- coding: utf-8 -*-
# @Author: li
# @Date:   2017-09-25 14:25:42
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2017-10-10 22:09:22
from setuptools import setup, find_packages

VERSION = '0.1.22'

setup(
    name='bilibiliSpiderSet',
    version=VERSION,
    description='A set of useful bilibili spider',
    author='Jiahuan Shi',
    author_email='redstonerock149@gmail.com',
    url='https://github.com/Haut-Stone',
    packages=['bilibiliSpiderSet'],
    include_package_data=True,
    install_requires=['requests>=2.12.4','beautifulsoup4>=4.5.1','html5lib>=0.999999999','click'],
    license='MIT License',
    zip_safe=False,
    entry_points={
          'console_scripts': [
              'avInfo = bilibiliSpiderSet.main:get_av_info',
              'upInfo = bilibiliSpiderSet.main:get_up_info',
              'liveBg = bilibiliSpiderSet.main:get_live_background',
              'cover = bilibiliSpiderSet.main:get_cover'
          ]
      },
)