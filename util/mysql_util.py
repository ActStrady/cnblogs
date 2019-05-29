#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# @Time : 2019/5/15 10:38
# @Author : ActStrady@tom.com
# @FileName : mysql_util.py
# @GitHub : https://github.com/ActStrady/spiders

import MySQLdb


def get_mysql_connect():
    host = '172.17.235.193'
    user = 'root'
    password = 'root'
    connect = MySQLdb.connect(host=host, user=user, password=password, charset='utf8')
    return connect
