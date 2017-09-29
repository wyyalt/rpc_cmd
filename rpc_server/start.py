import pika
import subprocess

credentials = pika.PlainCredentials('yun','yun@123')
parameters = pika.ConnectionParameters(host='119.29.237.13',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def exec_cmd(cmd):

    v = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = v.stdout.read()
    return result

def on_request(ch, method, props, body):
    cmd = body.decode('utf-8')

    print(" CMD:%s" % cmd)
    response = exec_cmd(cmd)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id,
                         delivery_mode = 2,
                     ),

                     body=response)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()