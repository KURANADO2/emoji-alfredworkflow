# !/usr/bin/python
# encoding: utf-8

import sys
from workflow import Workflow3, web
from multiprocessing.pool import ThreadPool
import urllib2
import os

ICON_DEFAULT = 'icon.png'
headers = {"Referer": "http://kuranado.com"}


def list_emoji(query=None):
    url = "http://api.kuranado.com/emoji/list"
    params = dict(keyword=query, page=1, size=9)

    r = web.get(url, params)

    # throw an error if request failed, Workflow will catch this and show it to the user
    r.raise_for_status()

    emojis = []
    data = r.json()

    path = "/tmp/emoji/"
    if not os.path.exists(path):
        os.makedirs(path)

    pool = ThreadPool(processes=4)

    for d in data['data']:

        image_name = d['url'][d['url'].index('emoji') + 6:]
        key_name = path + image_name
        d['path'] = key_name
        emojis.append(d)

        if os.path.exists(key_name):
            continue

        pool.apply_async(func=download, args=(d['url'], key_name))
    pool.close()
    pool.join()
    return emojis


def download(url, out_dir):

    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    if response.getcode() == 200:
        with open(out_dir, "wb") as f:
            f.write(response.read())
    else:
        logger.debug("图片下载失败")


def main(wf):
    if len(wf.args):
        query = wf.args[0]
    else:
        query = None

    # def wrapper():
    #     return list(query)
    #
    # emojis = wf.cached_data('list', wrapper, max_age=600)
    emojis = list_emoji(query)

    if len(emojis) <= 0:
        wf.add_item(title=u'未找到表情包', valid=True, icon=ICON_DEFAULT)

    # 添加 item 到 workflow 列表
    for emoji in emojis:
        wf.add_item(title=emoji['title'],
                    subtitle=emoji['path'],
                    arg=emoji['path'],
                    valid=True,
                    icon=emoji['path'],
                    quicklookurl=emoji['path'])

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()

    logger = wf.logger

    sys.exit(wf.run(main))
