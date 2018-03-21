# -*- coding: utf-8 -*-
# @Author: Haut-Stone
# @Date:   2018-03-03 21:41:04
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2018-03-03 22:29:08

import binascii  # 二进制和ASCII互相转换
import codecs  # 自然语言编码转换
import io  # 文件读写
import json
import os
import re
from xml.dom import minidom  # ???
from xml.etree import ElementTree as et

import qrcode
import requests
import rsa
from PIL import Image
from requests.utils import cookiejar_from_dict as dict2cookies  # 字典转cookies
from requests.utils import dict_from_cookiejar as cookies2dict  # cookies转字典


class BilibiliLogin():

    def __init__(self):
        '''
        Bilibili 登录类
        初始化时拥有所有API链接，请求用的头文件，一个Session会话，并且尝试连接，判断网络是否正常
        '''
        # 用户昵称
        self.user = ''
        self.qrcode_url = 'http://passport.bilibili.com/qrcode/getLoginUrl'
        self.qrcheck_url = 'http://passport.bilibili.com/qrcode/getLoginInfo'
        self.login_url = 'https://passport.bilibili.com/login'
        self.captcha_url = 'https://passport.bilibili.com/captcha'
        self.getkey_url = 'https://passport.bilibili.com/login?act=getkey'
        self.check_url = 'https://passport.bilibili.com/login/dologin'
        self.user_url = 'https://account.bilibili.com/home/userInfo'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/53.0.\
            2785.104',
            'Host': 'passport.bilibili.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,\
            image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': self.login_url,
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Proxy-Connection': 'keep-alive',
        }
        # 初始化时便自带了一个会话对象
        self.session = requests.Session()
        # cookies保存文件
        self.cookies_file = 'cookies.json'
        # 登录账号
        self.username = ''
        # 登录密码
        self.password = ''
        try:
            self.login_page = self.session.get(self.login_url)
            print('link start')
        except requests.exceptions.ConnectionError as e:
            print('link failed')

    def __loadCookies(self):
        '''
        如果不存在cookies或者读取错误，就让用户登录
        '''
        if not os.path.exists(self.cookies_file):
            print('Cookies file not exist, Please login first')
            return False
        try:
            with open(self.cookies_file, 'r') as fp:
                cookies = json.load(fp)
                self.session.cookies = dict2cookies(cookies)
                return True
        except:
            os.remove(self.cookies_file)
            print('Cookies file not exist, Please login first')
            return False

    def __getCaptcha(self):
        '''
        获取验证码并显示
        '''
        captcha = self.session.get(self.captcha_url, stream=True).content
        img = Image.open(io.BytesIO(captcha))
        img.show()

    def __isLogin(self):
        '''
        判断是否登录成功
        成功返回True
        失败返回False
        '''
        html = self.session.get(self.user_url).text
        params = json.load(html)
        code = params['code']
        if cood == 0:
            self.user = params['data']['uname']
            print('user %s login successed' % self.user)
            return True
        else:
            print('login failed')
            return False

    def __getRsaPwd(self, password):
        '''
        对密码进行加密
        '''
        response = self.session.get(self.getkey_url)
        token = json.loads(response.text)
        key = rsa.PublicKey.load_pkcs1_openssl_pem(token['key'])
        pwd = rsa.encrypt(text, key)
        pwd = binascii.b2a_base64(pwd)
        return pwd

    def __saveCookies(self):
        '''
        保存登录成功的Cookies到json文件中
        '''
        with open('cookies.json', 'wb') as fp:
            cookies = cookies2dict(self.session.cookies)
            fp.write(json.dumps(cookies, indent=True).encode('utf-8'))

    def normalLogin(self):
        '''
        通过 用户名 密码 验证码 形式登录 bilibili
        返回登录 session
        '''
        self.username = input('Please input username')
        self.password = input('Please input password')
        # 默认验证码为0
        captcha = '0'
        while captcha == '0':
            self.__getCaptcha()
            captcha = input('请输入验证码（输入0刷新验证码：')
        username = self.username
        password = self.__getRsaPwd(self.password)
        # 用户名，密码，验证码
        data = {
            'userid': username,
            'pwd': password,
            'vdcode': captcha,
        }
        print('loading.......\n')
        try:
            self.session.post(self.check_url, data=data)
        except requests.exceptions.ConnectionError as e:
            print('timeout!!')
        if self.__isLogin():
            self.__saveCookies()
        else:
            print('captchar or password wrong!!')

    def qrLogin(self):
        '''
        通过客户端扫描二维码登录
        '''
        while True:
            html = self.session.get(self.qrcode_url).text
            params = json.load(html)
            qr_url = params['data']['url']
            oauthKey = re.findall('oauthKey=(.*)', qr_url)[0]
            # 制作QR的过程
            qr = qrcode.QRCode(
                    version=2,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=1,
                )
            qr.add_data(qr_url)
            qr.make(fit=True)
            img = qr.make_image()
            img.show()
            op = input('按回车继续（输入0刷新二维码）：')
            if op != '0':
                break
        print('loading.....\n')
        self.session.post(self.qrcheck_url, data={'oauthKey': oauthKey})
        if self.__isLogin():
            self.__saveCookies()
        else:
            print('login failed!!')
