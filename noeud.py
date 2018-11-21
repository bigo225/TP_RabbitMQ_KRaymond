#!/usr/bin/env python
import pika
import sys
import time

class Node():
		                     
	if len(sys.argv) != 2:
		sys.stderr.write("Usage: %s [node Id] [node holder]\n" % sys.argv[0])
		sys.exit(1)
		
	if sys.argv[1] == '0':
		sys.stderr.write("Warning: [node Id] or [node holder] cannot be 0\n" %sys.argv[0])
		sys.exit(1)
		

	def __init__(self, node_id, node_holder):

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		    
		self.channel = self.connection.channel()
		self.channel.exchange_declare(exchange='direct',type='direct')
		
		self.result = channel.queue_declare(exclusive=True)
		self.queue_name = result.method.queue
		self.channel.queue_bind(exchange='direct', queue=queue_name)
		
		self.node_id = node_id
		#self.node_holder = int(sys.argv[2]) if sys.argv[2]!=sys.argv[1] else None
		self.node_holder = node_holder
		self.queue = []
		self.using=False  ## determine critical section state
		self.asked=False  ## determine if node has requested for token(privilège)

		pass


	##### Critical Section
	def request_section_critique(self, qeue_name):
		if self.node_holder != None:
		    self.queue.append(self.node_id)
		    if self.asked == False:
		        self.asked = True
			    self.channel.basic_publish(exchange='direct',
				        routing_key=qeue_name,
			            properties=pika.BasicProperties(reply_to = self.queue_name,),
	                    body=str(node_id))
			    print str(self.node_id)+" Sent request to holder "+str(self.node_holder)

			self.consume()

		using = True
		pass
		
	##### CONSUME
	def consume(self):
	    #channel.basic_qos(prefetch_count=1)
	    self.channel.basic_consume(self.callback,queue=self.queue_name)
	    self.channel.start_consuming()
		pass
		
	####Critical section
	def in_cs(self):
		print str(self.node_id)+" is in Critic section ..."
		time.sleep(20)
		print str(self.node_id)+" leave the Critic section ..."
		self.left_cs(self)
		pass
		
	##### left Critical Section
	def left_cs(self):
		self.using = False
		if self.queue:
			self.node_holder = self.queue.pop(0)[0]
			self.send_token()
			
			if self.queue:
				self.asked = True
				self.send_request()
		
		pass
	#### send request
	def send_request(self):
		channel.basic_publish(exchange='direct',
			          routing_key="",
			          properties=pika.BasicProperties(reply_to = self.queue_name,),
		              body=str(node_id))
		print str(self.node_id)+" Sent request to holder "+str(self.node_holder)
		
		pass
	
	### send token
	def send_token(self):
		self.channel.basic_publish(exchange='direct',
	                 routing_key="",
		             body="0")
		print str(self.node_id)+" Sent token to holder "+str(self.node_holder)

		pass
		
	##### has request
	def receive_request(self, sender, reply_to_queue):
	
		if self.node_holder == None and self.using==False:#si on est la racine
			self.node_holder = sender
			
			self.send_token(reply_to_queue)
		
		elif self.node_holder != sender: ## je ne suis pas la racine
			self.queue.append([sender,reply_to_queue])
			if self.asked==False:
				self.asked = True
				channel.basic_publish(exchange='direct',
		                      routing_key="",
		                      properties=pika.BasicProperties(reply_to = queue_name,),
		                      body=str(self.node_id))
				print " [x] Sent request to holder"
		
		pass

	##### has token
	def receive_token(self):
		temp = self.queue.pop(0)
		self.node_holder = temp[0]#le neoud pere devient le 1er elt de ma FA
		reply_to_queue = temp[1]
		
		if self.node_holder == self.node_id:## si je suis premier dans ma FA
			self.node_holder=None
		else:
			self.send_token(reply_to_queue)
		
			if queue:
				asked = True
				self.send_request(reply_to_queue)
				self.consume()
			else:
				asked = False
		pass




	### Callback
	def callback(self, ch, method, properties, body):
		if body =="0":
			self.receive_token()
			pass
		else:
			self.receive_request(body,properties.reply_to)
			pass
	
		print " [x] %r:%r" % (method.routing_key, body,)
		
		pass
	

