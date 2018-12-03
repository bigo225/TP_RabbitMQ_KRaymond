#!/usr/bin/env python
# -*- coding: latin-1 -*-

import pika
import sys
from node import Node

if len(sys.argv)<3 :
	sys.stderr.write("Usage: [node Id] [neighbour1 Id] [neighbour2 Id] ...\n")
	sys.exit(1)

if sys.argv[1] == '0':
	sys.stderr.write("Warning: [node Id] could not be an integer but 0\n")
	sys.exit(1)

if sys.argv[1] in sys.argv[2:]:
	sys.stderr.write("Warning: [node Id] could not be in neighbours list\n")
	sys.exit(1)

	
est_racine = raw_input("ce noeud est-il la racine?  O/N : ")
holder = False
node_id = int(sys.argv[1])
voisins = []
for i in sys.argv[2:]:
	voisins.append(int(i))

while(est_racine!= 'o' and est_racine !='O' and est_racine!= 'n' and est_racine !='N'):
	est_racine = input("ce noeud est-il la racine? Repondez par O(oui) ou N(non): ")

if est_racine== 'o' or est_racine =='O':
	holder = True



Node(node_id, voisins, holder)