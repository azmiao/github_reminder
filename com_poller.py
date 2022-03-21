import yaml
import os
from .get_com import *

# 判断是否有更新并返回相应的数据
# 以下注释是写给自己看的，当时没考虑好，导致for用的太多了，现在又不想改
async def jud_update():
    current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')
    file = open(current_dir, 'r', encoding="UTF-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    update_list = []
    replace_time = 0
    for uid in list(config['info'].keys()):
        # 当uid不是模板，且其有内容则检测更新
        if int(uid) != 123456789 and config['info'][uid] != None:
            # 对每个uid创建一个data信息
            data = {
                'uid': uid
            }
            # 对每个uid分别检索每个监控的url
            for dep_info in config['info'][uid]:
                # 获取该url和文件中存着的最新时间
                url = dep_info['url']
                init_time = dep_info['priv_time']
                init_time = datetime.strptime(str(init_time),"%Y-%m-%d %H:%M:%S")
                # 获取github上commit的最新时间
                html = await get_comHtml(url)
                link_list, n = await get_commits(html)  
                # link_list[0]就是第一个的时间
                priv_time = link_list[0]['com_time']
                priv_time = datetime.strptime(str(priv_time),"%Y-%m-%d %H:%M:%S")
                replace_time = priv_time
                # 比较两个时间，来判断是否有更新
                if priv_time > init_time:
                    # 判断出有更新了，所以在data下创建该url对应的空字典
                    data.setdefault(url,{})
                    # 既然有更新了，就得把在这5分钟内提交的commit全部弄出来
                    # 获取这个url的前5个commit，因为可能他总共就不到5个，所以用len()
                    for m in range(len(link_list)):
                        # 这个时间就是每个commit的时间了
                        priv_time = link_list[m]['com_time']
                        priv_time = datetime.strptime(str(priv_time),"%Y-%m-%d %H:%M:%S")
                        # 再拿这个时间和前面的文件时间比较
                        if priv_time > init_time:
                            # 说明这一条commit是在文件时间之后的
                            # 所以在data[url]里加入内容和作者的信息
                            data[url].setdefault(str(m), {})
                            data[url][str(m)].setdefault('com_time', priv_time)
                            data[url][str(m)].setdefault('com_str', link_list[m]['com_str'])
                            data[url][str(m)].setdefault('com_edit', link_list[m]['com_edit'])
                        # 如果没有就啥事不干，不过既然前面已经判断出有了，这里应该不可能没有了
            # 将这个uid下的所有信息写入到update_list里
            # 如果没有更新，那么这个data将是只有一个uid的字典
            update_list.append(data)
    # 返回的update_list是个有序list，里面每个元素都是data
    # 那么，如果一个uid没有数据更新，则len(data.keys())=1，如果有就是2
    # 且data[url]里的数据个数大于等于1
    return update_list, replace_time

async def update_broadcast(all_info):
    msg = f''
    for m in range(len(all_info)):
        com_time = all_info[str(m)]['com_time']
        com_str = all_info[str(m)]['com_str']
        com_edit = all_info[str(m)]['com_edit']
        msg = msg + f'\n▲{com_time} {com_edit}提交了 "{com_str}"'
    return msg

async def replace_info(uid, url, replace_time):
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
            data = {
                'url': url,
                'priv_time': replace_time
            }
            config_tmp['info'][uid].append(data)
    with open(current_dir, "w", encoding="UTF-8") as f:
        yaml.dump(config_tmp, f,allow_unicode=True)