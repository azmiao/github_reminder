import os
import json

from .get_com import create_msg
from .watch import watch_depo, unwatch_depo, query_depo, current_dir
from .com_poller import poller_update
from hoshino import Service, get_bot

# 首次启动不存在就创建文件
if not os.path.exists(current_dir):
    with open(current_dir, 'w', encoding="UTF-8") as f:
        json.dump({}, f, indent=4, ensure_ascii=False)

sv_help = '''命令如下：
(链接支持github镜像站)
[查仓库 仓库链接] 查该链接下的commits记录
[监控仓库 仓库链接] 监控该仓库，推送功能需另外开启
[不要监控仓库 仓库链接] 不再监控该仓库
[查询监控仓库] 查询自己监控的仓库列表
'''.strip()

# 默认对所有群关闭推送
sv = Service('github_reminder', help_=sv_help, enable_on_default=True)
svup = Service('github_reminder_poller', enable_on_default=False)

#帮助界面
@sv.on_fullmatch('github推送帮助')
async def help(bot, ev):
    await bot.send(ev, sv_help)

# 直接查询某仓库
@sv.on_prefix('查仓库')
async def search_depo(bot, ev):
    url = str(ev.message)
    try:
        msg = await create_msg(url)
    except Exception as e:
        msg = f'查询失败，错误：{e}'
    await bot.send(ev, msg)

# 监控
@sv.on_prefix('监控仓库')
async def watch_dep(bot, ev):
    gid, uid, url = str(ev.group_id), str(ev.user_id), str(ev.message)
    try:
        msg = await watch_depo(gid, uid, url)
    except Exception as e:
        msg = f'监控失败，错误：{e}'
    await bot.send(ev, msg)

# 取消监控
@sv.on_prefix('不要监控仓库')
async def unwatch_dep(bot, ev):
    gid, uid, url = str(ev.group_id), str(ev.user_id), str(ev.message)
    msg = await unwatch_depo(gid, uid, url)
    await bot.send(ev, msg)

# 查询监控仓库
@sv.on_fullmatch('查询监控仓库')
async def query_watched(bot, ev):
    gid, uid = str(ev.group_id), str(ev.user_id)
    msg = await query_depo(gid, uid)
    await bot.send(ev, msg)

# 推送commits更新
@svup.scheduled_job('cron', minute='*/5')
async def depo_commit_poller():
    bot = get_bot()
    try:
        await poller_update(bot)
    except Exception as e:
        svup.logger.info(f'检测commits更新失败，错误：{e}')