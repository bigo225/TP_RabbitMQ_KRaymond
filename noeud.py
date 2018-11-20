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
    
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

node_id = int(sys.argv[1])
node_holder = int(sys.argv[2]) if sys.argv[2]!=sys.argv[1] else None
queue = []
using=False  ## determine critical section state
asked=False  ## determine if node has requested for token(privilège)
#### define variables###



##### Critical Section



##### left Critical Section




##### Init
def initialize():
	pass


##### has request
def receive_request(int sender):
	
	if node_holder == None and using==False:
		node_holder = sender
		channel.basic_publish(exchange='direct_logs',
                      routing_key="token",
                      body="send token")
		print " [x] Sent token to holder"
		
	elif node_holder != sender:
		queue.append(sender)
		if asked==False:
			asked = True
			channel.basic_publish(exchange='direct_logs',
                          routing_key="request",
                          body=node_id)
			print " [x] Sent request to holder"
		


##### has token
def receive_token(sender):
	node_holder = queue[-1]
	queue.remove[node_holder]
	
	if node_holder == node_id:
		node_holder=None
	else:
		channel.basic_publish(exchange='direct_logs',
                      routing_key="token",
                      body="send token")
		print " [x] Sent token to holder"
		
		if queue:
			asked = True
			channel.basic_publish(exchange='direct_logs',
                      	  routing_key="request",
                          body="send token")
			print " [x] Sent request to holder"
		else:
			asked = False
	pass




### Callback
def callback(ch, method, properties, body):
    print " [x] %r:%r" % (method.routing_key, body,)
