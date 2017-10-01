import platform

rabbitMQ_user = 'yun'
rabbitMQ_pass = 'yun@123'
rabbitMQ_server = '119.29.237.13'

if platform.system() == "Windows":
    if_name = None
else:
    #linux网卡接口名称
    if_name = "eth0"

thread_count = 5