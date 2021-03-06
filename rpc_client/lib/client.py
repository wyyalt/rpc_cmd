import pika
import uuid
from src import execute

"""
可以对指定机器异步的执行多个命令
    例子：
    >>:run ""df -h"" --hosts 192.168.3.55 10.4.3.4 
    task id: 45334
    >>:check_task 45334 
    >>:
    注意，每执行一条命令，即立刻生成一个任务ID,不需等待结果返回，通过命令check_task TASK_ID来得到任务结果 "
作业重点:

使用RPC 实现，65
支持多台SERVER, 80
支持异步执行任务，90
"""

class Client(object):
    def __init__(self):
        self.credentials = pika.PlainCredentials('yun','yun@123')
        self.parameters = pika.ConnectionParameters(host='119.29.237.13',credentials=self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.response = None


    def set_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.connection.close()


    def publish(self, host_cmd,task_id):
        # self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=str(task_id),
            ),
            body=host_cmd
        )


    def consume(self,task_id=None):
        self.channel.basic_consume(
            self.set_response,
            no_ack=True,
            queue=self.callback_queue
        )

        while self.response is None:
            self.connection.process_data_events()

        return self.response

if __name__ == "__main__":
    cmd_rpc = Client()

    print(" [x] Requesting")
    cmd_rpc.publish("dir")
    response = cmd_rpc.consume()
    print(response.decode('gbk'))