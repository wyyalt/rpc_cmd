import pika
import subprocess
import socket
import settings
import threading
import struct
import fcntl


class Server(object):

    def __init__(self):
        self.ip_queue_name = self.get_address(if_name=None)
        self.credentials = pika.PlainCredentials(settings.rabbitMQ_user,settings.rabbitMQ_pass)
        self.parameters = pika.ConnectionParameters(host=settings.rabbitMQ_server,credentials=self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.ip_queue_name)

    def get_address(self,if_name=None):
        """
        返回内网ip
        """
        if if_name:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,
                struct.pack('256s', if_name[:15])
            )[20:24])
        else:
            return socket.gethostbyname(socket.gethostname())

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

def run():
    server_obj = Server()
    server_obj.consume()

if __name__ == "__main__":

    print("Waiting RPC requests")
    for i in range(settings.thread_count):
        t =  threading.Thread(target=run)
        t.start()

