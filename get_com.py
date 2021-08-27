import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta


# 获取仓库链接,暂时用不到，branch可选，以后要用再说
# def get_url(depo_owner, depo_name, branch):
#     url = f'https://github.com/{depo_owner}/{depo_name}/commits/{branch}'
#     return url, depo_name

# 返回commits界面的源码
def get_comHtml(url):
    req = urllib.request.Request(url)
    webpage = urllib.request.urlopen(req)
    html = webpage.read()
    return html

# 返回commits的信息
def get_commits(html):
    soup = BeautifulSoup(html, 'html.parser')
    link_list = []
    all_a_lable = soup.find_all('a')
    # 去除无用的a标签
    for a_lable in all_a_lable:
        if 'class' not in str(a_lable):
            all_a_lable.remove(a_lable)
    # 对所有a标签进行检索，获取相关信息
    for a_lable in all_a_lable:
        if a_lable.get('class') == ['Link--primary', 'text-bold', 'js-navigation-open', 'markdown-title'] and a_lable.string != 'Merge pull request':
            # commit时的标题
            if a_lable.string.startswith('from '):
                com_str = 'Merge pull request: ' + a_lable.string
            else:
                com_str = a_lable.string
            # commit的时间
            p0 = a_lable.get('href')
            other_list = re.findall(rf'{p0}.+?datetime="', str(html))
            another_list = re.findall(rf'{p0}.+?" class="no-wrap"', str(html))
            com_time = another_list[0].replace(f'{other_list[0]}', '')
            com_time = com_time.replace(f'" class="no-wrap"', '')
            priv_time = str(change_time(com_time))
            # commit的作者
            other_list_1 = re.findall(rf'{p0}.+?f6 color-text-secondary min-width-0">', str(html))
            another_list_1 = re.findall(rf'{p0}.+?committed', str(html))
            edit_html = another_list_1[0].replace(f'{other_list_1[0]}', '')
            edit_html = edit_html.replace(f'\n\n\n  committed', '')
            soup_tmp = BeautifulSoup(edit_html, 'html.parser')
            for a_lable_tmp in soup_tmp.find_all('a'):
                com_edit = a_lable_tmp.string
            # 整理数据结构，获取前5个commit数据，n为个数减1
            n = 4
            if len(link_list) <= n:
                data = {
                    'com_str': com_str,
                    'com_time': priv_time,
                    'com_edit': com_edit
                }
                link_list.append(data)
    return link_list, n

def change_time(raw_time):
    raw_time = str(raw_time).replace('Z', '')
    txtfmt = raw_time[:10]+ " " + raw_time[11:19]
    dt = datetime.strptime(txtfmt,"%Y-%m-%d %H:%M:%S")
    priv_time = dt + timedelta(hours=8)
    return priv_time

# 生成消息文本
def create_msg(url):
    html = get_comHtml(url)
    link_list, n = get_commits(html)
    msg = f'仓库{url}最近{n+1}次commit如下：'
    for link in link_list:
        com_time = link['com_time']
        com_edit = link['com_edit']
        com_str = link['com_str']
        msg = msg + f'\n▲{com_time} {com_edit}提交了 "{com_str}"'
    return msg

