
## 注意

由于需要在启动时接入翻译服务器，因此打开Hoshino的时候可能会在加载时卡一小会，不影响使用

其他功能在写了（

虽然不一定经常更新，但要不点个star支持一下？

## 更新日志

21-09-28    v1.5    新增马娘名/其他游戏术语替换，让翻译更加好康一点？

21-08-10    v1.4    翻译乱码修正，再新增头图显示，方便翻译卡池预告的时候看到马娘和支援卡的图片，BTW：手机QQ记得点开图片看不然显示不完整

21-08-04    v1.3    新增新闻翻译功能，但功能不太稳定，新增依赖需求看下面教程2安装

21-05-31    v1.2    05-15修复了插件卡死的bug，05-30修复了推送Bug(issues#2)，之前考试周+公会战没空测试，所以现在才更新

21-05-05    v1.1    代码重写，修复了播报不能用的BUG，现按时间戳排序，今天才发现官网新闻居然不是按照时间顺序排序的

21-05-01    v1.0    首次测试

## 使用前须知

1. 翻译出内容会受到你服务器所在地影响，不同地区连接到不同的翻译服务器，然后翻译出的结果不一样，我也不知道为啥，我这好像大多数没啥问题就不改了2333
    万一我以后遇到翻译问题我也会再改，如果你发现几个翻译问题可以再提交issue
    所以万一你觉得翻译的不太行，可以到`news_spider.py`的第147行，添加替换，可以替换翻译完的文本，比如米浴翻成了大米洗澡，你就可以添加一句：
```
news_text = news_text.replace('大米洗澡', '米浴')
```

2. v1.5新增了马娘名/其他游戏术语的文本替换，替换内容均在`replace_dict.json`里，后续好兄弟们觉得可以增加可以直接pull request

3. 如果只更新文件`replace_dict.json`的时候可直接热重载，更新完改文件后无需重新启动hoshinobot

## umamusume_news

一个适用hoshinobot的赛马娘新闻插件，用于提供马娘新闻播报功能

数据来自马娘官网

本插件仅供学习研究使用，插件免费，请勿用于商业用途，一切后果自己承担

## 项目地址：
https://github.com/azmiao/umamusume_news/

## 功能
```
正式功能：

[马娘新闻] 查看最近五条新闻

[新闻翻译] 查看翻译命令和新闻编号（限近5条）

[新闻翻译 1] 翻译第1条新闻，编号可选值(1/2/3/4/5)

（自动推送） 该功能没有命令
```
## 简单食用教程：

可看下方链接：

https://www.594594.xyz/2021/05/01/umamusume_news_for_hoshino/

或本页面：

1. 下载或git clone本插件：

在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
```
git clone https://github.com/azmiao/umamusume_news
```

2. 安装依赖：

到HoshinoBot\hoshino\modules\umamusume_news目录下，打开powershell运行
```
pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple
```

3. 在 HoshinoBot\hoshino\config\ `__bot__.py` 文件的 MODULES_ON 加入 'umamusume_news'

然后重启 HoshinoBot

4. 额外功能：（自动提醒）

在某个群里发消息输入下文以开启新闻播报
```
开启 umamusume-news-poller
```
可以通过发消息输入"lssv"查看这个功能前面是不是⚪来确认是否开启成功