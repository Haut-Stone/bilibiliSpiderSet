# -*- coding: utf-8 -*-
# @Author: li
# @Date:   2017-09-25 14:32:15
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2017-10-10 22:20:16
from bs4 import BeautifulSoup
import requests
import json
import re
import os

from .info import default_cookies, default_headers, default_kv
from .color_logger import Logger


'''
[文章url]
https://www.bilibili.com/read/cv19009
[live url]
https://live.bilibili.com/183
[av url]
https://www.bilibili.com/video/av15188459
'''


class CoverSpider():

	def get(self, raw_url):
		
		if re.match(r'^(https|http)://www.bilibili.com/video/av\d+', raw_url):
			return self.get_av_cover(raw_url)
		elif re.match(r'^(https|http)://www.bilibili.com/read/cv\d+', raw_url):
			return self.get_article_cover(raw_url)
		elif re.match(r'^(https|http)://live.bilibili.com/\d+', raw_url):
			return self.get_live_cover(raw_url)
		else:
			return {'error':'Wrong url'}

	def request(self, url, cookies=default_cookies, headers=default_headers, kv=default_kv):
		
		try:
			response = requests.get(url, headers=headers, cookies=cookies, params=kv)
			response.raise_for_status()
			response.encoding = response.apparent_encoding
			return response
		except:
			return {'error':"Unable to establish communication with this link"}


	def get_av_cover(self, url):
		
		response = self.request(url)
		if type(response) is dict:
			return response
		else:
			soup = BeautifulSoup(response.text, 'html5lib')
			cover_link = 'https:' + soup.find_all('img')[0].get('src')
			if cover_link is None:
				return {'error':"can't find cover_link"}
			else:
				return {'cover_link':cover_link}

	def get_article_cover(self, url):
		
		response = self.request(url)
		if type(response) is dict:
			return response
		else:
			soup = BeautifulSoup(response.text, 'html5lib')
			error = soup.find_all('div', class_='error')
			if len(error) is 0:
				js = soup.find_all('script')[0].text
				if js is None:
					return {'error':'啊咧？没有诶!'}
				else:
					return {'cover_link':js.split('"')[7]}
			else:
				return {'error':'这篇文章并不存在'}

	def get_live_cover(self, url):
		
		room_id = re.findall(r'\d+', url)[0]
		api_url = 'https://api.live.bilibili.com/AppRoom/index' 
		kv = {
			'device':'phone',
			'platform':'ios',
			'scale':'3',
			'build':'10000',
			'room_id':str(room_id),
		}

		response = self.request(api_url, kv=kv)
		if type(response) is dict:
			return response
		else:
			info = json.loads(response.text)
			return {'cover_link':info['data']['cover']}

class UpInfoSpider():

	def request(self, url, kv):
		headers = {'User-Agent':'Mozilla/5.0'}
		try:
			r = requests.get(url, params=kv, headers=headers, timeout=3)
			r.raise_for_status()
			r.encoding = 'utf-8'
			return r
		except:
			Logger.fail('无法与这个链接建立通讯')

	def analysis(self, response):
		bs = BeautifulSoup(response.text, 'html5lib')
		up_infos = {'sum':0,'upusers':[]}
		for up in bs.find_all(attrs={'class': 'up-item'}):
			upface = up.find_all('div')[0]
			name = upface.a['title']
			imgUrl = 'https:' + upface.a.img['data-src']
			upinfo = up.find_all('div')[1].find_all('div')[2].find_all('span')
			videoNum = re.findall("\d+",upinfo[0].get_text())[0]
			fansNum = re.findall("\d+",upinfo[1].get_text())[0]
			up_info = {
				'name':name,
				'video_num':videoNum,
				'fans_num':fansNum,
				'img_url':imgUrl,
			}
			up_infos['sum'] = up_infos['sum'] + 1
			up_infos['upusers'].append(up_info)
		return up_infos

	def get_top_20_up_info(self, user_name):
		pre_link = 'https://search.bilibili.com/upuser'
		kv = {
			'keyword':str(user_name)
		}
		response = self.request(pre_link, kv)
		if response == None:
			return None
		else:
			info = self.analysis(response)
			return info

# 爬取直播界面的背景图片，并保存
class Xspider():

	def main(self, url, save):
		response = self.request(url)
		if response == None:
			Logger.warning('没有获取到任何信息哦')
		else:
			soup = self.analysis(response)
			if save:
				self.save_bg(soup, url)
			else:
				bg_info = soup.find('div', class_='bk-img w-100 h-100')
				if bg_info == None:
					Logger.warning('这个页面被锁定了，里面没有信息')
				else:
					bg_link = bg_info['style'][22:-1]
					if bg_link[0] == '/':
						bg_link = 'https:' + bg_link
						return {'bglink':bg_link}
					else:
						Logger.warning('这个图片是bilibili官方提供的，被跳过了 = \
							= ')

	def request(self, url):
		headers = {'User-Agent':'Mozilla/5.0'}
		try:
			r = requests.get(url, timeout=5, headers=headers)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
			return r.text
		except:
			Logger.fail('无法与这个链接建立通讯')
	def analysis(self, response):
		soup = BeautifulSoup(response, 'lxml')
		return soup

	def save_bg(self, soup, url):
		name = url.split('/')[-1]
		# 这里的路径改成本机路径就可以使用了
		path = '/Users/li/Desktop/' + name + '.jpg'
		bg_info = soup.find('div', class_='bk-img w-100 h-100')
		if bg_info == None:
			Logger.warning('这个页面被锁定了，里面没有信息')
		else:
			bg_link = bg_info['style'][22:-1]
			if bg_link[0] == '/':
				bg_link = 'https:' + bg_link
				try:
					headers = {'User-Agent':'Mozilla/5.0'}
					img = requests.get(bg_link, headers=headers)
					img.raise_for_status()
					with open(path, 'wb') as f:
						f.write(img.content)
						f.close()
						Logger.ok('YES! 图片 %s 号已经被保存到桌面了' % name)
				except:
					Logger.fail('啦咧？无法保存图片')
			else:
				Logger.warning('这个图片是bilibili官方提供的，被跳过了 = = ')
