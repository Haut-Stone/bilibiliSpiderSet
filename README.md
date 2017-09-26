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

>现在这个爬虫合集一共有六只爬虫，另外还有爬取会员的世界的爬虫正在测试中。

下面的代码都是直接在终端里输入就可以了。举个例子，如果我想获得av7视频的封面，那么我只用在终端中
，直接输入下面这个一行代码，av7的封面地址就会直接被终端打印出来了。

```bash
avCover 7
```
![](使用演示.gif)

获取普通投稿视频的信息（会员的世界和番剧除外）

```bash
avInfo '视频的av号'
```

获取普通投稿视频的封面

```bash
avCover '视频的av号'
```

获取bilibili专栏文章的封面

```bash
articleCover '专栏文章的url'
```

获取直播间的封面

```bash
liveCover '直播间的房间号'
```

获取符合条件的前20个up的信息

```bash
upInfo 'up的名字'
```

获取直播间的背景图片（官方图片会被直接跳过）

```bash
liveBg '直播间的url'
```

## 感谢

- [读取命令行参数](http://wiki.jikexueyuan.com/project/explore-python/Standard-Modules/argparse.html)
- [读取命令行参数](http://www.jianshu.com/p/a50aead61319)
- [通过pip发布](https://segmentfault.com/a/1190000008663126)
- [学习实例（感谢这位大牛）](https://github.com/twocucao/danmu.fm)
- [完整处理过程](http://www.jianshu.com/p/eb27d5cb5e1d)
- [click库](http://click.pocoo.org/5/)
- [Click库的使用方法](https://segmentfault.com/a/1190000007858815)
- [如何使用github标签](http://blog.csdn.net/yangbodong22011/article/details/51791085)