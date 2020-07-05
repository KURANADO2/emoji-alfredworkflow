# !/usr/bin/python
# encoding: utf-8

import sys
from workflow import Workflow3

ICON_DEFAULT = 'icon.png'


def main(wf):

    if wf.update_available:
        wf.add_item('有可用的新版本',
                    '回车安装新版本',
                    autocomplete='workflow:update',
                    icon=ICON_DEFAULT)
    else:
        wf.add_item('暂无可用新版本',
                    icon=ICON_DEFAULT)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3(update_settings={
        'github_slug': 'KURANADO2/emoji-alfredworkflow',
        '__workflow_autoupdate': True,
        # 自动检测新版本频率，单位 day
        'frequency': 1
    })

    logger = wf.logger

    sys.exit(wf.run(main))
