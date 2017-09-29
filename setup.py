# -*- coding: utf-8 -*-
# @Author: li
# @Date:   2017-09-25 14:25:42
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2017-09-28 22:51:36
from setuptools import setup, find_packages

VERSION = '0.1.12'

setup(
    name='bilibiliSpiderSet',
    version=VERSION,
    description='A set of useful bilibili spider',
    author='Jiahuan Shi',
    author_email='redstonerock149@gmail.com',
    url='https://github.com/Haut-Stone',
    packages=['bilibiliSpiderSet'],
    include_package_data=True,
    install_requires=['requests>=2.12.4','beautifulsoup4>=4.5.1','html5lib>=0.999999999'],
    license='MIT License',
    zip_safe=False,
    entry_points={
          'console_scripts': [
              'avInfo = bilibiliSpiderSet.main:get_av_info',
              'avCover = bilibiliSpiderSet.main:get_av_cover',
              'articleCover = bilibiliSpiderSet.main:get_articel_cover',
              'liveCover = bilibiliSpiderSet.main:get_live_cover',
              'upInfo = bilibiliSpiderSet.main:get_up_info',
              'liveBg = bilibiliSpiderSet.main:get_live_background',
              'avCover_vip = bilibiliSpiderSet.main:get_av_cover_vip',
          ]
      },
)