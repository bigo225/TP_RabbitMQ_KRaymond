#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
        
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         type='direct')
                         
if len(sys.argv) != 2:
    sys.stderr.write("Usage: %s [node Id] [node holder]\n" % sys.argv[0])
    sys.exit(1)
    
node_id = sys.argv[1]
node_holder = sys.argv[2]


#### define variables###



##### Critical Section



##### left Critical Section




##### Init




##### has request




##### has token
