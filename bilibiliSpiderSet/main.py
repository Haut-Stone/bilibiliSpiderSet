# -*- coding: utf-8 -*-
# @Author: li
# @Date:   2017-09-25 19:10:55
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2017-09-28 22:20:29

from .bilibiliSpiderSet import AVInfoSpider, ArticelImageSpider
from .bilibiliSpiderSet import Xspider, UpInfoSpider
from .bilibiliSpiderSet import LiveCoverSpider, FuckBilibiliSpider
from .bilibiliSpiderSet import cookies
import argparse


def get_av_info():

	parser = argparse.ArgumentParser()
	parser.add_argument('av_number', type=int, help='input av number to get info')
	args = parser.parse_args()

	spider = AVInfoSpider()
	info = spider.get_Info(args.av_number)
	if info != None:
		print(info)

def get_av_cover():

	parser = argparse.ArgumentParser()
	parser.add_argument('av_number', type=int, help='input av number to get cover')
	args = parser.parse_args()

	spider = AVInfoSpider()
	link = spider.get_cover_link(args.av_number)
	if link != None:
		print(link)

def get_articel_cover():

	parser = argparse.ArgumentParser()
	parser.add_argument('url', type=str, help='input articel to get cover')
	args = parser.parse_args()

	spider = ArticelImageSpider()
	link = spider.main(args.url)
	if link != None:
		print(link)

def get_live_cover():

	parser = argparse.ArgumentParser()
	parser.add_argument('room_id', type=int, help='input room_id to get cover')
	args = parser.parse_args()

	spider = LiveCoverSpider()
	link = spider.get_cover_link(args.room_id)
	if link != None:
		print(link)

def get_up_info():

	parser = argparse.ArgumentParser()
	parser.add_argument('up_name', type=str, help='input up name to get up info')
	args = parser.parse_args()

	spider = UpInfoSpider()
	info = spider.get_top_20_up_info(args.up_name)
	if info != None:
		print(info)

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
		print(link)

def get_av_cover_vip():

	parser = argparse.ArgumentParser()
	parser.add_argument('av_number', type=int, help='input av_number to get cover')
	args = parser.parse_args()

	spider = FuckBilibiliSpider()
	info = spider.get_Info(args.av_number, cookies=cookies)
	if info != None:
		print(info)