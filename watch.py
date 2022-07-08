import os
import json

from .get_com import get_commits

# 监控信息文件
current_dir = os.path.join(os.path.dirname(__file__), 'config.json')

# 监控
async def watch_depo(gid, uid, url):
    with open(current_dir, 'r', encoding="UTF-8") as f:
        file_data = json.load(f)
    group_info = file_data.get(gid, {})
    user_info = group_info.get(uid, {})
    if user_info.get(url, {}): return '你已经监控过该仓库了，无需再次监控'
    data_list = await get_commits(url)
    priv_time = str(data_list[0]['time'])
    user_info[url] = priv_time
    group_info[uid] = user_info
    file_data[gid] = group_info
    with open(current_dir, 'w', encoding="UTF-8") as f:
        json.dump(file_data, f, indent=4, ensure_ascii=False)
    return f'您已成功在群{gid}里监控仓库：{url}'

# 取消监控
async def unwatch_depo(gid, uid, url):
    with open(current_dir, 'r', encoding="UTF-8") as f:
        file_data = json.load(f)
    group_info = file_data.get(gid, {})
    user_info = group_info.get(uid, {})
    if not user_info.get(url, {}): return '你还未监控过该仓库，请先使用命令监控'
    file_data[gid][uid].pop(url)
    with open(current_dir, 'w', encoding="UTF-8") as f:
        json.dump(file_data, f, indent=4, ensure_ascii=False)
    return f'您已成功在群{gid}里取消监控仓库：{url}'

# 监控查询
async def query_depo(gid, uid):
    with open(current_dir, 'r', encoding="UTF-8") as f:
        file_data = json.load(f)
    group_info = file_data.get(gid, {})
    user_info = group_info.get(uid, {})
    return '您暂未监控任何仓库呢！' if not user_info else '您所监控的仓库有：\n' + '\n'.join(list(user_info.keys()))