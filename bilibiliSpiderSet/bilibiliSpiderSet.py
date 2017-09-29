# -*- coding: utf-8 -*-
# @Author: li
# @Date:   2017-09-25 14:32:15
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2017-09-28 22:50:46
from bs4 import BeautifulSoup
import requests
import re
import os
import json

class AVInfoSpider():

	def request(self, url):
		headers = {'User-Agent':'Mozilla/5.0 '}
		try:
			r = requests.get(url, headers=headers, timeout=3)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
			return r
		except:
			print('无法与这个链接建立通讯')

	def analysis(self, response):
		bs = BeautifulSoup(response.text, 'html5lib')
		link = bs.find_all('img')[0].get('src')
		if link == None:
			print('这个视频不存在,或者是会员的世界')
			return None
		else:
			title = bs.find_all('h1')[0].get('title')
			contents = bs.find_all('meta')
			author = contents[3].get('content')
			dic = {'link':'https:' + link, 'title':title, 'author':author,}
			return dic

	def get_Info(self, avNumber):
		url = 'http://www.bilibili.com/video/av' + str(avNumber)
		response = self.request(url)
		if response == None:
			return None
		else:
			info_dic = self.analysis(response)
			return info_dic

	def get_cover_link(self, avNumber):
		info_dic = self.get_Info(avNumber)
		if info_dic == None:
			return None
		else:
			return {'link':info_dic['link']}

class LiveCoverSpider():

	def request(self, url, kv):
		headers = {'User-Agent':'Mozilla/5.0'}
		try:
			r = requests.get(url, params=kv, headers=headers, timeout=3)
			r.raise_for_status()
			r.encoding = 'utf-8'
			return r
		except:
			print('无法与这个链接建立通讯')

	def get_cover_link(self, room_id):
		pre_link = 'https://api.live.bilibili.com/AppRoom/index'
		kv = {
			'device':'phone',
			'platform':'ios',
			'scale':'3',
			'build':'10000',
			'room_id':str(room_id),
		}
		response = self.request(pre_link, kv)
		if response == None:
			return None
		else:
			info = json.loads(response.text)
			return info['data']['cover']

class UpInfoSpider():

	def request(self, url, kv):
		headers = {'User-Agent':'Mozilla/5.0'}
		try:
			r = requests.get(url, params=kv, headers=headers, timeout=3)
			r.raise_for_status()
			r.encoding = 'utf-8'
			return r
		except:
			print('无法与这个链接建立通讯')

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
			print("没有获取到任何信息哦")
		else:
			soup = self.analysis(response)
			if save:
				self.save_bg(soup, url)
			else:
				bg_info = soup.find('div', class_='bk-img w-100 h-100')
				if bg_info == None:
					print("这个页面被锁定了，里面没有信息")
				else:
					bg_link = bg_info['style'][22:-1]
					if bg_link[0] == '/':
						bg_link = 'https:' + bg_link
						return {'bglink':bg_link}
					else:
						print('这个图片是bilibili官方提供的，被跳过了 = = ')

	def request(self, url):
		headers = {'User-Agent':'Mozilla/5.0'}
		try:
			r = requests.get(url, timeout=5, headers=headers)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
			return r.text
		except:
			print("好可惜，无法与网页 %s 建立通讯 " % url.split('/')[-1])

	def analysis(self, response):
		soup = BeautifulSoup(response, 'lxml')
		return soup

	def save_bg(self, soup, url):
		name = url.split('/')[-1]
		# 这里的路径改成本机路径就可以使用了
		path = '/Users/li/Desktop/' + name + '.jpg'
		bg_info = soup.find('div', class_='bk-img w-100 h-100')
		if bg_info == None:
			print("这个页面被锁定了，里面没有信息")
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
						print('YES! 图片 %s 号已经被保存到桌面了' % name)
				except:
					print('啦咧？无法保存图片')
			else:
				print('这个图片是bilibili官方提供的，被跳过了 = = ')


# bilibili的专栏封面爬虫
class ArticelImageSpider():

	def request(self, url):
		headers = {'User-Agent':'Mozilla/5.0'}
		try:
			r = requests.get(url, headers=headers)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
			return r.text
		except:
			print('无法与这个链接建立通讯')

	def analysis(self, response):
		soup = BeautifulSoup(response, 'html5lib')
		error = soup.find_all('div', class_='error')
		if len(error) == 0:
			js = soup.find_all('script')[0].text
			if js == None:
				print('啊咧？没有诶!')
				return None
			else:
				return js.split('"')[7]
		else:
			print('这个链接并不存在')
			return None	

	def main(self, url):
		response = self.request(url)
		if response == None:
			return None
		else:
			img_url = self.analysis(response)
			info = {'img_url':img_url}
			return info


class FuckBilibiliSpider():

	def request(self, url, cookies):
		headers = {
			'User-Agent':'Mozilla/5.0'
		}
		try:
			r = requests.get(url, headers=headers, cookies=cookies, timeout=3)
			r.raise_for_status()
			r.encoding = r.apparent_encoding
			return r
		except:
			print('无法与这个链接建立通讯')

	def analysis(self, response):
		bs = BeautifulSoup(response.text, 'html5lib')
		link = bs.find_all('img')[0].get('src')
		if link == None:
			print('这个视频不存在,或者是会员的世界')
			return None
		else:
			title = bs.find_all('h1')[0].get('title')
			contents = bs.find_all('meta')
			author = contents[3].get('content')
			dic = {'link':'https:' + link, 'title':title, 'author':author,}
			return dic

	def get_Info(self, avNumber, cookies):
		url = 'http://www.bilibili.com/video/av' + str(avNumber)
		response = self.request(url, cookies)
		if response == None:
			return None
		else:
			info_dic = self.analysis(response)
			return info_dic

	def get_cover_link(self, avNumber):
		info_dic = self.get_Info(avNumber)
		if info_dic == None:
			return None
		else:
			return {'link':info_dic['link']}



cookies = {
	'DedeUserID': '221013145',
	'DedeUserID__ckMd5': '0ada37d8e37bee1f',
	'SESSDATA': 'ddff3d5b%2C1508937653%2C5dc59211'
}



