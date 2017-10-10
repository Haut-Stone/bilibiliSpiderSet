# -*- coding: utf-8 -*-
# @Author: li
# @Date:   2017-09-25 19:10:55
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2017-10-10 22:08:34

import argparse
import click

from .spider_set import Xspider, UpInfoSpider
from .spider_set import CoverSpider
from .color_logger import Logger

def get_up_info():

	parser = argparse.ArgumentParser()
	parser.add_argument('up_name', type=str, help='input up name to get up info')
	args = parser.parse_args()

	spider = UpInfoSpider()
	info = spider.get_top_20_up_info(args.up_name)
	if info != None:
		ups = info['upusers']
		for up in ups:
			Logger.ok(up['name'])
			Logger.ok(up['video_num'])
			Logger.ok(up['fans_num'])
			Logger.ok(up['img_url'])

def get_live_background():

	parser = argparse.ArgumentParser()
	parser.add_argument('room_url', type=str, help='input room url to get cover')
	parser.add_argument('-s', '--save', type=str, choices=['T', 'F'], help='inp\
						ut save path to save background (default : desktop)')
	args = parser.parse_args()
	if args.save == 'T':
		save = True
	else:
		save = False
	spider = Xspider()
	link = spider.main(args.room_url,save)
	if link != None:
		Logger.ok(link['bglink'])

@click.command()
@click.argument('url', type=str, required=True)
def get_cover(url):

	spider = CoverSpider()
	info = spider.get(url)
	if 'error' in info.keys():
		Logger.fail(info['error'])
	else:
		Logger.ok(info['cover_link'])