import pika
import subprocess
import socket
import settings

class Server(object):

    def __init__(self):
        self.ip_queue_name = socket.gethostbyname(socket.gethostname())
        self.credentials = pika.PlainCredentials(settings.rabbitMQ_user,settings.rabbitMQ_pass)
        self.parameters = pika.ConnectionParameters(host=settings.rabbitMQ_server,credentials=self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.ip_queue_name,exclusive=True)


    def exec_cmd(self,cmd):
        """
        命令执行函数
        :param cmd:客户端发送的cmd
        :return: 执行结果
        """
        v = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        result = v.stdout.read()+v.stderr.read()
        return result

    def publish(self,ch, method, props, body):
        """
        发布结果
        """
        cmd = body.decode('utf-8')
        print("Command>>%s" % cmd)
        response = self.exec_cmd(cmd)
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id,
                delivery_mode = 2,
                message_id=self.ip_queue_name
            ),
            body=response
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        """
        订阅消息
        """
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.publish, queue=self.ip_queue_name)
        self.channel.start_consuming()

if __name__ == "__main__":
    server_obj = Server()
    print("Waiting RPC requests")
    server_obj.consume()