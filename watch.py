import yaml
import os
from .get_com import *

current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')

async def watch_depo(uid, url):
    with open(current_dir, 'r', encoding="UTF-8") as f:
        file_data = f.read()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    if uid not in config['info'].keys():
        config['info'].setdefault(uid,[])
    html = await get_comHtml(url)
    link_list, n = await get_commits(html)
    priv_time = link_list[0]['com_time']
    data = {
        'url': url,
        'priv_time': priv_time
    }
    config['info'][uid].append(data)
    with open(current_dir, "w", encoding="UTF-8") as f:
        yaml.dump(config, f,allow_unicode=True)
    msg = f'成功监控仓库：{url}'
    return msg

async def unwatch_depo(uid, url):
    with open(current_dir, 'r', encoding="UTF-8") as f:
        file_data = f.read()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    config_tmp = config
    for info_data in config['info'][uid]:
        if info_data['url'] == url:
            data = {
                'url': url,
                'priv_time': info_data['priv_time']
            }
            config_tmp['info'][uid].remove(data)
    with open(current_dir, "w", encoding="UTF-8") as f:
        yaml.dump(config, f,allow_unicode=True)
    url = await back_url(url)
    msg = f'成功取消监控仓库：{url}'
    return msg

async def query_depo(uid):
    with open(current_dir, 'r', encoding="UTF-8") as f:
        file_data = f.read()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    if len(config['info'][uid]) == 0:
        msg = '您暂未监控任何仓库呢！'
    else:
        msg = '您所监控的仓库有：'
        for info_data in config['info'][uid]:
            url = await back_url(info_data['url'])
            msg = msg + f'\n{url}'
    return msg

# 获取真实commit的url链接
async def get_true_commit_url(url):
    url_pattern = re.compile(f'(https://github.com/\S+/\S+/)tree(/\S+)')
    url_tmp = re.match(url_pattern, url)
    if url_tmp:
        url = url_tmp.group(1) + 'commits' + url_tmp.group(2)
    else:
        url += '/commits'
    return url

# 还原url链接
async def back_url(url):
    url_pattern = re.compile(f'(https://github.com/\S+/\S+/)commits(/\S+)')
    url_tmp = re.match(url_pattern, url)
    if url_tmp:
        url = url_tmp.group(1) + 'tree' + url_tmp.group(2)
    else:
        url = url.replace('/commits','')
    return url