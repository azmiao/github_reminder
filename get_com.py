import re
import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# 调整太平洋时间
async def change_time(raw_time):
    raw_time = str(raw_time).replace('Z', '')
    txtfmt = raw_time[:10]+ " " + raw_time[11:19]
    dt = datetime.strptime(txtfmt,"%Y-%m-%d %H:%M:%S")
    cur_time = dt + timedelta(hours=8)
    return cur_time

# 返回commits的信息
async def get_commits(url):
    # 获取真实URL
    url_tmp = re.match(fr'(https://github.com/\S+/\S+/)tree(/\S+)', url)
    url = url + '/commits' if not url_tmp else url_tmp.replace('tree', 'commits')
    # 读取代理
    with open(os.path.join(os.path.dirname(__file__), 'account.json')) as fp:
        pinfo = json.load(fp)
    proxy = pinfo['proxy']
    data_list = []
    resp = requests.get(url=url, proxies = proxy, timeout=20)
    soup = BeautifulSoup(resp.text, 'lxml')
    block_list = soup.find_all('li', {"class": "Box-row Box-row--focus-gray mt-0 d-flex js-commits-list-item js-navigation-item js-socket-channel js-updatable-content"})
    for block in block_list[:5]:
        if block.find('span', {"class": "hidden-text-expander inline"}):
            block.find('span', {"class": "hidden-text-expander inline"}).decompose()
        cur_time = await change_time(block.find('relative-time').get('datetime'))
        data_list.append({
            'title': block.find('p', {"class": "mb-1"}).text.strip(),
            'author': block.find('a', {"class": "commit-author user-mention"}).text,
            'time': cur_time
        })
    return data_list

# 生成消息文本
async def create_msg(url):
    data_list = await get_commits(url)
    msg = f'仓库{url}最近5次commit如下：'
    for data in data_list:
        title = data['title']
        author = data['author']
        time = data['time']
        msg += f'\n▲{time} {author}提交了 "{title}"'
    return msg