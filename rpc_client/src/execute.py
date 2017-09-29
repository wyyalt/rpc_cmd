import re
from lib import client
import random

class Execute(object):


    def __init__(self):


        self.queue_name = None
        self.task_dict = {}
        """
        task_dict = {
            11111:{
                
            }
        }
        """


    def create_task_id(self):
        task_id = random.randint(10000, 99999)

        while True:
            if task_id in self.task_dict:
                self.create_task_id()
            else:
                print(task_id)
                return task_id

    def route(self,user_input):
        """
        命令分发函数
        :return: 1.错误信息 2.用户执行结果
        """

        self.user_input = user_input
        if self.user_input.startswith("run "):
            cmd_flag = re.search('"[^"]*"', self.user_input)
            if not cmd_flag:
                return "缺少命令参数"
            else:
                host_cmd = cmd_flag.group().strip('"')

            host_flag = re.search('--hosts', self.user_input)
            if not host_flag:
                return "缺少--hosts关键字"
            else:
                host_list = re.findall('(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})', self.user_input)
                if not host_list:
                    return "主机列表不能为空"
                else:
                    self.host_list = host_list
                    return self.run(host_cmd)

        elif self.user_input.startswith("check_task "):
            task_id = re.search('\d{5}', user_input).group().strip()
            if task_id:
                return self.check_task(task_id)
                # 反射

        else:
            if self.user_input.split(" ")[0] == 'check_all':
                return self.check_all()
                # 反射
            else:
                return "命令输入错误"

    def run(self,host_cmd):
        """
        命令执行函数
        :param host_cmd: 远程命令
        :param host_list: 主机列表
        :return:
        """
        print(host_cmd,self.host_list)
        self.client = client.Client()
        task_id = self.create_task_id()
        self.client.publish(host_cmd,task_id,'task_response')


    def check_task(self,task_id):
        """
        查看单个任务执行结果
        :param task_id:任务ID
        :return:
        """
        print(task_id,self.host_list)
        self.client = client.Client()
        result = self.client.consume('task_response',task_id)
        return result.decode("gbk")

    def check_all(self):
        """
        查看所有任务执行结果
        :return: 所有任务执行结果
        """
        print("check_all")



if __name__ == "__main__":
    #run "df -h" --hosts 127.0.0.1 10.0.0.2
    while True:
        user_input = input(">>").strip()
        obj = Execute(user_input)
        result = obj.route()
        print(result)



