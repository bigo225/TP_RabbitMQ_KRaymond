#!/usr/bin/env python
# -*- coding: latin-1 -*-

import pika
import sys
import time

class Node():

	def __init__(self, node_id, voisins, holder= False, recovery= False):

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		    
		self.channel = self.connection.channel()
		self.channel.exchange_declare(exchange='direct',exchange_type='direct')
		
		self.result = self.channel.queue_declare(exclusive=True)
		self.queue_name = self.result.method.queue
		self.channel.queue_bind(exchange='direct', queue=self.queue_name, routing_key=str(node_id))
		
		self.voisins = voisins 
		self.node_id = int(node_id)
		self.queue = []
		self.using=False  ## determine critical section state
		self.asked=False  ## determine if node has requested for token(privilège)
		self.is_consuming=False
		self.in_recovery = recovery
		self.donnees = []
		
		if holder:
			self.node_holder = None
			self.send_initialize(self.voisins)

		elif self.in_recovery:
			self.send_restart(self.voisins)
		else:
			self.consume()
	
	###intialization
	def send_initialize(self, voisins):
		for v in voisins:
			self.channel.basic_publish(exchange='direct',
						 routing_key=str(v),
						 body="-1 "+str(self.node_id))
			print str(self.node_id)+" Sent initialize to voisin "+str(v)
			#time.sleep(3)
		self.consume()
		pass
	
	def receive_initialize(self, holder):
		print str(self.node_id)+" received INITIALIZE message from holder "+str(holder)
		self.node_holder = int(holder)
		print str(self.node_id)+" set holder to "+str(self.node_holder)
		#si je ne suis pas une feuille
		if len(self.voisins)!=1:
			voisins=[]
			for v in self.voisins:
				if self.node_holder != int(v):
					voisins.append(v)
			self.send_initialize(voisins)
	
	##### Critical Section --- demande d'entrer en section critique
	def request_section_critique(self):
		if self.node_holder != None: ## je ne suis pas la racine
		    self.queue.append(self.node_id) ##je m'ajoute dans ma FA
		    ## si je n'ai pas dejà demander le privilège, je la demande
		    if self.asked == False: 
		        self.asked = True
		        self.send_request()
		#je suis la racine, j'entre directement en CS
		else:
			self.in_cs()

	##### CONSUME
	def consume(self):
	    #channel.basic_qos(prefetch_count=1)
	    #time.sleep(3)
	    self.channel.basic_consume(self.callback,queue=self.queue_name)
	    if not self.is_consuming:
			self.is_consuming=True
			self.channel.start_consuming()
		
	####Critical section
	def in_cs(self):
		self.using = True
		print str(self.node_id)+" is in Critical section ..."
		time.sleep(15)
		print str(self.node_id)+" leave the Critical section ..."
		self.left_cs()
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
		else:
			self.consume()
		
		pass
	#### send request
	def send_request(self):
		self.channel.basic_publish(exchange='direct',
			          routing_key=str(self.node_holder),
		              body=str(self.node_id))
		print str(self.node_id)+" Sent REQUEST message to holder "+str(self.node_holder)
		# j'attends la reponse
		self.consume()
		
		pass
	
	### send token
	def send_token(self):
		self.channel.basic_publish(exchange='direct',
	                 routing_key=str(self.node_holder),
		             body="0")
		print str(self.node_id)+" Sent TOKEN to holder "+str(self.node_holder)

		pass
	
	### send restart
	def send_restart(self, voisins):
		for v in voisins:
			self.channel.basic_publish(exchange='direct',
		                 routing_key=str(v),
			             body="-4 "+str(self.node_id))
			print str(self.node_id)+" Sent RESTART message to neighbour "+str(v)
			#time.sleep(3)
		self.consume()

	#send advice
	def send_advise(self, sender):
		in_my_queue = False
		is_my_node_holder = False

		if int(sender) in self.queue:
			in_my_queue == True

		if self.node_holder == int(sender):
			is_my_node_holder = True
		self.channel.basic_publish(exchange='direct',
	                 routing_key=str(sender),
		             body="-3"+" "+str(self.node_id)+" "+str(is_my_node_holder)+" "+str(in_my_queue)+" "+str(self.asked))
		print str(self.node_id)+" Sent advise message to node "+str(sender)
		self.consume()

	###receive restart message
	def receive_restart(self, sender):
		print str(self.node_id)+" received RESTART message from neighbour "+str(sender)	
		self.send_advise(sender)
		pass

	## receive advise
	def receive_advise(self, donnee):
		print str(self.node_id)+" received ADVISE message from neighbour "+str(donnee[0])
		self.donnees.append(donnee)
		if len(self.donnees) == len(self.voisins):
			## on determine le holder
			n=0
			for result in self.donnees:
				if result[1] == 'True':
					n+=1
					# reconstruction de la queue
					if result[3] == 'True':
						self.queue = int(result[0])
				else:
					self.node_holder = int(result[0])
					print str(self.node_id)+" set holder to "+str(self.node_holder)

			if n==len(self.voisins):
				self.node_holder = None
				print str(self.node_id)+" is the root"
				if self.using == False and self.asked == False and self.queue:
					self.node_holder = self.queue.pop(0)
					if self.node_holder == self.node_id:## si je suis premier dans ma FA 
						self.node_holder=None
						self.in_cs()
			else:
				self.send_token()
			
				if self.queue:
					self.asked = True
					self.send_request()
				else:
					self.asked = False


			# On determine son etat asked
			if self.node_holder == None:
				self.asked = False
			else:
				for liste in self.donnees:
					if self.node_holder in liste:
						if self.donnees[self.donnees.index(liste)][2] == 'True':
							self.asked = True
							print str(self.node_id)+" had asked for token"
							break
			self.recovery = False
		else:
			self.consume()
				
	##### has request
	def receive_request(self, sender):
		
		### si je ne suis pas en mode recovery
		if not self.in_recovery:
			#si on est la racine et que je ne suis pas en section critique
			if self.node_holder == None and self.using==False:
				self.node_holder = sender
				self.asked = False	
				self.send_token() #je renvoi le jeton
			
			elif self.node_holder != None: ## je ne suis pas la racine
				self.queue.append(sender) ## j'ajoute à ma FA le sender de la requete
				if self.asked==False:
					self.asked = True
					self.send_request()
		else:
			self.queue.append(sender)
		pass

	##### has token
	def receive_token(self):
		### si je ne suis pas en mode recovery
		if not self.in_recovery:
			print str(self.node_id)+" received TOKEN message from neighbour "+str(self.node_holder)
			self.node_holder = self.queue.pop(0)# le 1er elt de ma FA devient le neoud pere 
			
			if self.node_holder == self.node_id:## si je suis premier dans ma FA 
				self.node_holder=None
				self.in_cs()
			else:
				self.send_token()
			
				if self.queue:
					self.asked = True
					self.send_request()
				else:
					self.asked = False
		else:
			self.node_holder=None
			print str(self.node_id)+" received TOKEN message from neighbour "+str(self.node_holder)
			if self.node_holder == self.node_id:## si je suis premier dans ma FA
				self.in_cs()


	### Callback
	def callback(self, ch, method, properties, body):
		time.sleep(3)
		if body =="0":
			self.receive_token()
			pass
		
		elif body.split(' ')[0] == '-1':
			self.receive_initialize(body.split(' ')[1])
			pass

		elif body == '-2':
			print str(self.node_id)+" needs to get in critical section "
			self.request_section_critique()
			pass

		elif body.split(' ')[0] == '-3':
			liste = body.split(' ')[1:]
			self.receive_advise(liste)
			pass

		elif body.split(' ')[0] == '-4':
			self.receive_restart(body.split(' ')[1])
			pass

		else:
			self.receive_request(body)