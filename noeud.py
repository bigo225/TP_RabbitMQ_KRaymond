#!/usr/bin/env python
# -*- coding: latin-1 -*-

import pika
import sys
import time

class Node():
		                     
	if len(sys.argv) != 3:
		sys.stderr.write("Usage: %s [node Id] [node holder]\n" % sys.argv[0])
		sys.exit(1)
		
	if sys.argv[1] == '0' or sys.argv[2] == '0':
		sys.stderr.write("Warning: [node Id] or [node holder] cannot be 0\n")
		sys.exit(1)
		

	def __init__(self, node_id, node_holder):

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		    
		self.channel = self.connection.channel()
		self.channel.exchange_declare(exchange='direct',exchange_type='direct')
		
		self.result = channel.queue_declare(exclusive=True)
		self.queue_name = result.method.queue
		self.channel.queue_bind(exchange='direct', queue=queue_name, routing_key=str(node_id))
		
		self.node_id = node_id
		self.node_holder = node_holder
		if self.node_holder == self.node_id:
			self.node_holder = None
		self.queue = []
		self.using=False  ## determine critical section state
		self.asked=False  ## determine if node has requested for token(privilège)
		pass


	##### Critical Section --- demande d'entrer en section critique
	def request_section_critique(self, qeue_name):
		if self.node_holder != None: ## je ne suis pas la racine
		    self.queue.append(self.node_id) ##je m'ajoute dans ma FA
		    ## si je n'ai pas dejà demander le privilège, je la demande
		    if self.asked == False: 
		        self.asked = True
		        self.self.send_request()
			
			#j'attends la reponse(le jeton)
			self.consume()
		#je suis la racine, j'entre directement en CS
		else:
			self.in_cs()
			pass
		
		pass
		
	##### CONSUME
	def consume(self):
	    #channel.basic_qos(prefetch_count=1)
	    self.channel.basic_consume(self.callback,queue=self.queue_name)
	    self.channel.start_consuming()
	    pass
		
	####Critical section
	def in_cs(self):
		self.using = True
		print str(self.node_id)+" is in Critic section ..."
		time.sleep(20)
		print str(self.node_id)+" leave the Critic section ..."
		self.left_cs(self)
		pass
		
	##### left Critical Section
	def left_cs(self):
		self.using = False
		#je verifie ma FA
		if self.queue:
			self.node_holder = self.queue.pop(0)
			self.send_token()
			
			if self.queue:
				self.asked = True
				self.send_request()
		
		pass
	#### send request
	def send_request(self):
		channel.basic_publish(exchange='direct',
			          routing_key=str(node_holder),
		              body=str(node_id))
		print str(self.node_id)+" Sent request to holder "+str(self.node_holder)
		# j'attends la reponse
		self.consume()
		
		pass
	
	### send token
	def send_token(self):
		self.channel.basic_publish(exchange='direct',
	                 routing_key=str(node_holder),
		             body="0")
		print str(self.node_id)+" Sent token to holder "+str(self.node_holder)

		pass
		
	##### has request
	def receive_request(self, sender):
		#si on est la racine et que je ne suis pas en section critique
		if self.node_holder == None and self.using==False:
			self.node_holder = sender
			self.send_token() #je renvoi le jeton
		
		elif self.node_holder != None: ## je ne suis pas la racine
			self.queue.append(sender) ## j'ajoute à ma FA le sender de la requete
			if self.asked==False:
				self.asked = True
				self.send_request()
				
		
		pass

	##### has token
	def receive_token(self):
		self.node_holder = self.queue.pop(0)#le neoud pere devient le 1er elt de ma FA
		
		if self.node_holder == self.node_id:## si je suis premier dans ma FA
			self.node_holder=None
		else:
			self.send_token()
		
			if queue:
				asked = True
				self.send_request()

			else:
				asked = False
		pass




	### Callback
	def callback(self, ch, method, properties, body):
		if body =="0":
			self.receive_token()
			pass
		else:
			self.receive_request(body)
			pass
	
		print " [x] %r:%r" % (method.routing_key, body,)
		
		pass
	

