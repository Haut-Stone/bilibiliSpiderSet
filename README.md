## 快捷的bilibili命令行爬虫

[![DUB](https://img.shields.io/dub/l/vibe-d.svg)]()
[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)]()
[![PyPI](https://img.shields.io/pypi/v/nine.svg)]()

这是一个用来爬取bilibili部分信息的命令行工具

>持续更新中，喜欢的话来个star呗 (｡･ω･｡)

### 通过pip安装

现在只测试了Mac用户,Mac用户可以很方便的通过pip进行下载。在终端中输入如下代码即可。

```bash
pip3 install bilibiliSpiderSet
```

### 使用方法

>现在这个爬虫合集一共有3只爬虫.

下面的代码都是直接在终端里输入就可以了。举个例子，如果我想获得av7视频的封面，那么我只用在终端中
，直接输入下面这个一行代码，av7的封面地址就会直接被终端打印出来了。`cover命令现在可以支持视频（包括会员的世界），直播，专栏的封面链接获取`

```bash
cover https://www.bilibili.com/video/av7/
```

获取符合条件的前20个up的信息

```bash
upInfo 'up的名字'
```

获取直播间的背景图片（官方图片会被直接跳过）

```bash
liveBg '直播间的url'
```

## 让程序使用它

当然，你还可以直接让你的程序调用`bilibiliSpiderSet`中的爬虫类，创建爬虫实例，从而在程序中运用爬虫集合中的爬虫。
例如你可以这样去新建一个爬虫对象
```python
spider = CoverSpider()
info = spider.get('https://www.bilibili.com/video/av7/')
```
这里的所有爬虫类中的方法都会返回标准的字典建值对，方便我们将数据打包成json文件
## 感谢

- [读取命令行参数](http://wiki.jikexueyuan.com/project/explore-python/Standard-Modules/argparse.html)
- [读取命令行参数](http://www.jianshu.com/p/a50aead61319)
- [通过pip发布](https://segmentfault.com/a/1190000008663126)
- [学习实例（感谢这位大牛）](https://github.com/twocucao/danmu.fm)
- [完整处理过程](http://www.jianshu.com/p/eb27d5cb5e1d)
- [click库](http://click.pocoo.org/5/)
- [Click库的使用方法](https://segmentfault.com/a/1190000007858815)
- [如何使用github标签](http://blog.csdn.net/yangbodong22011/article/details/51791085)

## 作者

[@Haut-Stone](https://github.com/Haut-Stone)由☕️，🍜，🍛，🍕，🍔，🍙，🍢，🍪，🍺，🍶，🍣，🍖强力驱动