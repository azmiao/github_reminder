import yaml
import os
from .get_com import *

def watch_depo(uid, url):
    current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')
    file = open(current_dir, 'r', encoding="UTF-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    if uid not in config['info'].keys():
        config['info'].setdefault(uid,[])
    html = get_comHtml(url)
    link_list, n = get_commits(html)
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

def unwatch_depo(uid, url):
    current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')
    file = open(current_dir, 'r', encoding="UTF-8")
    file_data = file.read()
    file.close()
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
    url = url.replace('/commits', '')
    msg = f'成功取消监控仓库：{url}'
    return msg

def query_depo(uid):
    current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')
    file = open(current_dir, 'r', encoding="UTF-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    if len(config['info'][uid]) == 0:
        msg = '您暂未监控任何仓库呢！'
    else:
        msg = '您所监控的仓库有：'
        for info_data in config['info'][uid]:
            url = info_data['url'].replace('/commits','')
            msg = msg + f'\n{url}'
    return msg