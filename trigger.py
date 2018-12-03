#!/usr/bin/env python
# -*- coding: latin-1 -*-

import pika
import sys

if len(sys.argv)!=2 :
	sys.stderr.write("Usage: [node Id]\n")
	sys.exit(1)
		
if sys.argv[1] == '0':
	sys.stderr.write("Warning: [node Id] could not be an integer but 0\n")
	sys.exit(1)
	
node_id = sys.argv[1]

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
result = channel.queue_declare(exclusive=True)


### send need criticaal section
channel.basic_publish(exchange='direct',
				   routing_key=str(node_id),
				   body="-2")
print " messasge sent to "+str(node_id)