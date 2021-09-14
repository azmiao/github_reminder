import re
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

# 返回commits界面的源码
def get_comHtml(url):
    try:
        req = urllib.request.Request(url)
        webpage = urllib.request.urlopen(req, timeout=10)
        html = webpage.read()
    except:
        html = '链接超时！请尝试使用镜像站或稍后尝试'
    return html

# 返回commits的信息
def get_commits(html):
    soup = BeautifulSoup(html, 'html.parser')
    link_list = []
    n = 0
    all_a_lable = soup.find_all('a')
    # 去除无用的a标签
    for a_lable in all_a_lable:
        if 'class' not in str(a_lable):
            all_a_lable.remove(a_lable)
    # 对所有a标签进行检索，获取相关信息
    for a_lable in all_a_lable:
        if a_lable.get('class') == ['Link--primary', 'text-bold', 'js-navigation-open', 'markdown-title'] and a_lable.string != 'Merge pull request' and a_lable.string != ')':
            # commit时的标题
            # 判断string是否为空，为空就取text文本
            if a_lable.string != None:
                # 判断merge pull的情况
                if a_lable.string.startswith('from '):
                    com_str = 'Merge pull request: ' + a_lable.string
                # 判断 issue的编号
                elif a_lable.string.endswith(' ('):
                    # print(str(a_lable))
                    a_lable_t = str(a_lable).replace('(', '\(')
                    a_lable_t = a_lable_t.replace('/', '\/')
                    a_lable_temp = re.findall(r'' + a_lable_t + r'.+?<\/a>', str(html))
                    # print(str(a_lable_temp))
                    if a_lable_temp != []:
                        a_lable_temp = a_lable_temp[0]
                        a_lable_temp = a_lable_temp.replace(f'{a_lable}', '')
                        soup_do = BeautifulSoup(str(a_lable_temp), 'html.parser')
                        down_a_lable = soup_do.find('a')
                        issue_str = ''
                        if down_a_lable.get('class') == ['issue-link', 'js-issue-link']:
                            issue_str = down_a_lable.string
                        com_str = a_lable.string + 'issue ' + issue_str + ')'
                # 正常情况
                else:
                    com_str = a_lable.string
            # 非正常情况，可能其中有<code></code>时使用text
            else:
                com_str = a_lable.text
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
    if html == '链接超时！请尝试使用镜像站或稍后尝试':
        return html
    link_list, n = get_commits(html)
    msg = f'仓库{url}最近{n+1}次commit如下：'
    for link in link_list:
        com_time = link['com_time']
        com_edit = link['com_edit']
        com_str = link['com_str']
        msg = msg + f'\n▲{com_time} {com_edit}提交了 "{com_str}"'
    return msg

