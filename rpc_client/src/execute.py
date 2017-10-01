import re
import json
import random
from lib import client
from conf import settings

class Execute(object):

    def __init__(self):
        self.task_dict = json.load(open(settings.task_dict, "r"))
        self.task_list = json.load(open(settings.task_list, "r"))

    def create_task_id(self):
        """
        生成TaskID
        :return: task_id
        """
        task_id = random.randint(10000, 99999)

        while True:
            if task_id in self.task_dict:
                self.create_task_id()
            else:
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
                return "Command parameter missing!"
            else:
                host_cmd = cmd_flag.group().strip('"')

            host_flag = re.search('--hosts', self.user_input)
            if not host_flag:
                return "Missing --hosts keywords!"
            else:
                host_list = re.findall('(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})', self.user_input)
                if not host_list:
                    return "The host list cannot be empty!"
                else:
                    self.host_list = host_list
                    return self.run(host_cmd)

        elif self.user_input.startswith("check_task "):
            try:
                task_id = re.search('\d{5}', user_input).group().strip()
            except Exception:
                return "Command input error!"

            if task_id:
                return self.check_task(task_id)
        else:
            if self.user_input.split(" ")[0] == 'check_all':
                return self.check_all()
            else:
                return "Command input error!"

    def run(self,host_cmd):
        """
        命令执行函数
        :param host_cmd: 远程命令
        :param host_list: 主机列表
        :return:TIPS
        """
        self.client = client.Client()
        task_id = self.create_task_id()
        for ip_queue_name in self.host_list:
            self.client.publish(host_cmd,task_id,ip_queue_name,'task_response')

        self.task_dict[str(task_id)] = {'command':host_cmd}
        self.task_list.append(str(task_id))

        with open(settings.task_dict,'w') as f:
            json.dump(self.task_dict,f)

        #ID极限值
        while len(self.task_list) > settings.id_count:
            del self.task_dict[self.task_list[0]]
            del self.task_list[0]

        with open(settings.task_list, 'w') as f:
            json.dump(self.task_list, f)

        print("TaskID:%s"%task_id)
        return "Command execution successful. Please use check_task 'id' to see the result！"


    def check_task(self,task_id):
        """
        查看单个任务执行结果
        :param task_id:任务ID
        :return:单个ID执行结果
        """
        if task_id in self.task_dict:
            result_flag = False
            consume_flag = False
            result = self.task_dict[task_id].get('command_result')
            if not result:
                consume_flag = True
                self.client = client.Client()
                result = self.client.consume('task_response',task_id)

            for k,v in result.items():
                if k == "Error":
                    return "\r\n Failed Error! \r\n %s\r\n" %(v)
                else:
                    result_flag = True
                    print("\r\n[ServerIP:%s] \r\n\r\n %s"%(k,v))

            if result_flag and consume_flag:
                self.task_dict[task_id]['command_result'] = result
                with open(settings.task_dict, 'w') as f:
                    json.dump(self.task_dict, f)

            return "Print Done"
        else:
            return "The input ID does not exist!"

    def check_all(self):
        """
        查看所有任务执行结果
        :return: 所有任务执行结果
        """
        for k,v in enumerate(self.task_list):
            print("SN:%s TaskID:%s Command:%s"%(k,v,self.task_dict[v]['command']))

        return "Print Done!"



if __name__ == "__main__":
    #run "df -h" --hosts 127.0.0.1 10.0.0.2
    pass


