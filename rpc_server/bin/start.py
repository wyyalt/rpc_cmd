#/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import gevent

import threading
from lib import server
from conf import settings

def run():
    server_obj = server.Server()
    server_obj.consume()

def new_run():
    run()

if __name__ == "__main__":

    print("Waiting RPC requests")
    for i in range(settings.thread_count):
        t =  threading.Thread(target=run)
        t.start()

    gevent.joinall([
        gevent.spawn(run),
        gevent.spawn(new_run)
    ])
