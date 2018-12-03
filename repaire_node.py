#!/usr/bin/env python
# -*- coding: latin-1 -*-

import pika
import sys
from node import Node

if len(sys.argv)<3 :
	sys.stderr.write("Usage: %s [node Id] [node holder] [voisin1] [voisin2] ...\n")
	sys.exit(1)
		
if sys.argv[1] == '0':
	sys.stderr.write("Warning: [node Id] could not be an integer but 0\n")
	sys.exit(1)
	
if sys.argv[1] in sys.argv[2:]:
	sys.stderr.write("Warning: [node Id] could not be in neighbours list\n")
	sys.exit(1)

node_id = sys.argv[1]

voisins = []
for i in sys.argv[2:]:
	voisins.append(int(i))

Node(node_id, voisins, recovery = True)