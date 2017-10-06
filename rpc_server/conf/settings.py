#/usr/bin/python
# -*- coding: utf-8 -*-

import platform

#rabbitmq服务器相关信息
rabbitMQ_user = 'yun'
rabbitMQ_pass = 'yun@123'
rabbitMQ_server = '119.29.237.13'

if platform.system() == "Windows":
    if_name = None
else:
    #linux网卡接口名称
    if_name = "eth0"

#开线程数
thread_count = 5

if __name__ == "__main__":
    print(platform.system())