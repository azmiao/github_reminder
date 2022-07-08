
## 注意

插件后续将继续在 github 更新，欢迎提交 isuue 和 request

※ 提交issue反馈bug麻烦提供日志，并说明清楚

## 更新日志

22-07-08    v2.0.0  删了原来的垃圾代码，重写了一份，因此需要删除`confg.yml`文件再更新，且需要重新监控仓库，试图解决[issue #8](https://github.com/azmiao/github_reminder/issues/8)

22-03-21    v1.4.1  全部改为异步进行，[issue #6](https://github.com/azmiao/github_reminder/issues/6)

21-11-09    v1.4    跟随github源码更新修复一个小bug，(github居然偷偷改源码了23333)

21-09-14    v1.3    修复string中含有其他代码引发的报错(issue #1),并增加了查仓库issue编号的判断

21-09-06    v1.2    应该修复了可能进程卡死的问题

## github_reminder

一个适用hoshinobot的 github仓库更新提醒 插件

## 项目地址：

https://github.com/azmiao/github_reminder

## 功能

```
命令如下：
(链接支持github镜像站)
[查仓库 仓库链接] 查该链接下的commits记录
[监控仓库 仓库链接] 监控该仓库，推送功能需另外开启
[不要监控仓库 仓库链接] 不再监控该仓库
[查询监控仓库] 查询自己监控的仓库列表

(自动推送监控的仓库更新，需要手动开启)
```

## 简单食用教程：

1. git clone本插件：

    在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
    ```
    git clone https://github.com/azmiao/github_reminder
    ```

2. 设置代理（可选）

    默认不启用代理！

    打开 `account.json`：（默认状态）
    ```
    {
        "proxy": {}
    }
    ```

    如果您的服务器在国内，那建议开启代理：

    打开 `account.json`：（开启代理状态）

    其中 1081 为代理的端口号，请自行查找你的代理的端口号并替换上
    ```
    {
        "proxy": {
            "http": "http://localhost:1081",
            "https": "http://localhost:1081"
        }
    }
    ```

2. 安装依赖，到HoshinoBot\hoshino\modules\github_reminder目录下，管理员方式打开powershell
    ```
    pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple
    ```

3. 在 HoshinoBot\hoshino\config\ `__bot__.py` 文件的 MODULES_ON 加入 'github_reminder'

    然后重启 HoshinoBot

4. 在某一群内发送 “开启 github_reminder_poller” 即可启用自动推送功能

    群内发送 'github推送帮助' 可获取更多帮助