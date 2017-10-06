import os,sys,platform
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

task_dict = os.path.join(BASE_DIR,'db','task_dict.log')
task_list = os.path.join(BASE_DIR,'db','task_list.log')

#存储taskid最大值
id_count = 50

#rabbitmq服务器相关信息
rabbitMQ_user = 'yun'
rabbitMQ_pass = 'yun@123'
rabbitMQ_server = '119.29.237.13'

#编码设置不需要手动修改
if platform.system() == "Windows":
    body_code = "gbk"
else:
    body_code = "utf-8"