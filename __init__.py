from hoshino import Service
from hoshino.util import FreqLimiter
from .get_com import *
from .watch import *
from .com_poller import *
import re

_limtime = 10    # 单个人查询冷却时间（单位：喵）
_flmt = FreqLimiter(_limtime)

sv_help = '''命令如下：
(链接支持github镜像站)

[查仓库 仓库链接] 查该链接下的commits记录

[监控仓库 仓库链接] 监控该仓库，推送功能需另外开启

[不要监控仓库 仓库链接] 不再监控该仓库

[查询监控仓库] 查询自己监控的仓库列表

其他：

(自动推送监控的仓库更新)'''.strip()

# 默认对所有群关闭
sv = Service('github_reminder', help_=sv_help, enable_on_default=True)
svup = Service('github_reminder_poller', enable_on_default=False)

#帮助界面
@sv.on_fullmatch('github推送帮助')
async def help(bot, ev):
    await bot.send(ev, sv_help)

# 直接查询某仓库
@sv.on_prefix('查仓库')
async def search_depo(bot, ev):
    uid = ev['user_id']
    if not _flmt.check(uid):
        await bot.send(ev, f'请勿频繁操作，冷却时间为{_limtime}秒！', at_sender=True)
        return
    url = ev.message.extract_plain_text()
    url = await get_true_commit_url(url)
    msg = await create_msg(url)
    await bot.send(ev, msg)

# 监控
@sv.on_prefix('监控仓库')
async def watch_dep(bot, ev):
    uid = ev['user_id']
    url = ev.message.extract_plain_text()
    url = await get_true_commit_url(url)
    try:
        msg = await watch_depo(uid, url)
    except:
        msg = '未知错误！监控失败！'
    await bot.send(ev, msg)

# 取消监控
@sv.on_prefix('不要监控仓库')
async def unwatch_dep(bot, ev):
    uid = ev['user_id']
    url = ev.message.extract_plain_text()
    url = await get_true_commit_url(url)
    try:
        msg = await unwatch_depo(uid, url)
    except:
        msg = '取消监控失败！请确保你已监控该仓库，或请稍等一分钟再试一次'
    await bot.send(ev, msg)

# 查询监控仓库
@sv.on_fullmatch('查询监控仓库')
async def query_watched(bot, ev):
    uid = ev['user_id']
    try:
        msg = await query_depo(uid)
    except:
        msg = '查询失败，请稍后再试'
    await bot.send(ev, msg)

# 推送commits更新
@svup.scheduled_job('cron', minute='*/5')
async def depo_commit_poller():
    try:
        update_list, replace_time = await jud_update()
    except:
        svup.logger.info(f'检测commits更新失败，偶尔发生属于正常现象不用慌，经常发生请反馈bug')
        return
    flag = 0
    # 每个uid
    for all_info in update_list:
        if len(all_info.keys()) != 1:
            flag = 1
            uid = all_info['uid']
            msg = f'[CQ:at,qq={uid}]\n'
            url_list = list(all_info.keys())[1:]
            for url in url_list:
                url_tmp = await back_url(url)
                msg = msg + f'\n◎您监控的{url_tmp}有如下commit更新：\n'
                svup.logger.info(f'检测到{uid}监控的Url有commit更新！')
                msg += await update_broadcast(all_info[url])
                await replace_info(uid, url, replace_time)
            await svup.broadcast(msg, 'github_reminder-poller', 0.2)
    if flag == 0:
        svup.logger.info(f'暂未检测到commit更新')