
## 注意

插件后续将继续在 github 更新，欢迎提交 isuue 和 request

其他功能慢慢开发，要摸鱼

## 更新日志

21-08-23    v1.0    大概能用了？

## github_reminder

一个适用hoshinobot的 github仓库更新提醒 插件

本插件仅供学习研究使用，插件免费，请勿用于违法商业用途，一切后果自己承担

## 项目地址：

https://github.com/azmiao/github_reminder

## 功能

```
命令如下：
(链接支持github镜像站)

[查仓库 仓库链接] 查该链接下的commits记录

[监控仓库 仓库链接] 监控该仓库，推送功能需另外开启

[不要监控 仓库链接] 不再监控该仓库

其他：

(自动推送监控的仓库更新，需要手动开启)
```
```
一个例子:

监控仓库 https://github.dihe.moe/pcrbot/HoshinoBot-plugins-index

这将监控 这个地核镜像站的插件索引目录
然后再手动开启github_reminder_poller就会有推送了
```

## 简单食用教程：

可看下方链接（还没写）：

https://www.594594.xyz/2021/08/24/github_reminder_for_hoshino/

或本页面：

1. 下载或git clone本插件：

    在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
    ```
    git clone https://github.com/azmiao/github_reminder
    ```

2. 在 HoshinoBot\hoshino\config\ `__bot__.py` 文件的 MODULES_ON 加入 'github_reminder'

    然后重启 HoshinoBot

3. 在某一群内发送 “开启 github_reminder_poller” 即可启用自动推送功能

    群内发送 'github推送帮助' 可获取更多帮助
