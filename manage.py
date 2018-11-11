#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from app import create_app

from flask_script import Manager

import config
import os
import traceback
import urllib.request, urllib.parse, urllib.error

app = create_app()
manager = Manager(app)


@manager.command
def list_routes():
    """打印出配置的 url 列表（模块、http method、url）"""
    output = get_routes()
    for item in output:
        line = urllib.parse.unquote(
            "{:50s} {:20s} {}".format(
                item['endpoint'],
                item['methods'],
                item['url'])
        )
        print(line)


def get_routes():
    """获取配置的 url 列表（模块、http method、url）"""
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = str(rule)

        item = {
            'endpoint': rule.endpoint,
            'methods': methods,
            'url': url
        }
        output.append(item)

    return output


@manager.command
def join_lines(path, wrap=""):
    """连接每行内容"""

    with open(path, "r") as f:
        lines = []
        for line in f:
            line = line.strip()
            if wrap:
                line = wrap + line + wrap
            lines.append(line)

        print((",".join(lines)))


@manager.command
def debugserver(host=config.DEV_HOST, port=config.DEV_PORT):
    """启动测试服务器"""
    if isinstance(port, str) and port.isdigit():
        port = int(port)
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug=True, host=host, port=port)


@app.errorhandler(500)
def internal_server_error(errors):
    trace = traceback.format_exc()
    from flask import request
    return '500 Internal Server Error'


if __name__ == '__main__':
    manager.run()
