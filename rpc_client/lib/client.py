import pika
from conf import settings

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
        self.credentials = pika.PlainCredentials(settings.rabbitMQ_user,settings.rabbitMQ_pass)
        self.parameters = pika.ConnectionParameters(host=settings.rabbitMQ_server,credentials=self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.response = {}
        # result = self.channel.queue_declare(queue='task_response')
        # result = self.channel.queue_declare(exclusive=True)
        # self.callback_queue = result.method.queue



    def set_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response[props.message_id] = body.decode(settings.body_code)

            ch.basic_ack(
                delivery_tag=method.delivery_tag
            )


    def publish(self, host_cmd,task_id,pub_queue_name,queue_name):
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_publish(
            exchange='',
            routing_key=pub_queue_name,
            properties=pika.BasicProperties(
                reply_to=queue_name,
                correlation_id=str(task_id),
            ),
            body=host_cmd
        )

    def consume(self,queue_name,task_id=None):
        self.corr_id = task_id
        self.channel.basic_consume(
            self.set_response,
            queue=queue_name
        )

        while not self.response:
            self.connection.process_data_events()
            if not self.response:
                self.response["Error"]="Command execute failed!"
                break

        self.connection.close()
        return self.response


if __name__ == "__main__":
    pass