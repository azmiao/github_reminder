import json
import asyncio
from datetime import datetime

from .get_com import get_commits
from .watch import current_dir
from hoshino import logger

# 判断是否有更新并推送
async def poller_update(bot):
    with open(current_dir, 'r', encoding="UTF-8") as f:
        file_data = json.load(f)
    for gid in list(file_data.keys()):
        for uid in list(file_data[gid].keys()):
            if not file_data[gid][uid]: continue
            msg = f'[CQ:at,qq={uid}]\n'
            for url in list(file_data[gid][uid].keys()):
                await asyncio.sleep(0.5)
                old_time = datetime.strptime(file_data[gid][uid][url],"%Y-%m-%d %H:%M:%S")
                data_list = await get_commits(url)
                new_time = data_list[0]['time']
                if new_time <= old_time: continue
                msg += f'\n◎您监控的仓库{url}检测到如下commit更新：'
                logger.info(f'检测到群{gid}的{uid}监控的仓库{url}有更新')
                # 该URL更新了
                for data in data_list:
                    data_time = data['time']
                    if data_time > old_time:
                        msg += f'\n▲{data["time"]} {data["author"]}提交了 "{data["title"]}"'
                # 替换监控信息的时间为最新commit时间
                file_data[gid][uid][url] = str(new_time)
            if msg != f'[CQ:at,qq={uid}]\n':
                await bot.send_group_msg(group_id=gid, message=msg)
    with open(current_dir, 'w', encoding="UTF-8") as f:
        json.dump(file_data, f, indent=4, ensure_ascii=False)