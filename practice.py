from blockchain import blockexplorer
from decimal import *
import requests
import operator
import datetime
import hashlib
# import util

print '\n\n\n\n\n\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'



def explore_address(address):
	print 'TODO'

# Gets $USD of 1 bitcoin
def get_conversion_rate():
	timestamp = datetime.datetime.now()

	# This url returns the value of bitcoin for the given amount of USD
	USD_URL = 'https://blockchain.info/tobtc'
	payload = {'currency': 'USD', 'value': '100'}
	r = requests.get(USD_URL, params=payload)

	x = float(r.text)
	dollars = 100.0 / x
	print dollars
	return (timestamp, dollars)


def get_transaction_amount(tx):
	print 'get_transaction_amount'
	outputs = tx.outputs

	val = 0
	for o in outputs:
		val += o.value

	print val
	return val

######################################################################

# THIS IS ALL BLOCKHAIN STUFF

#####################################################################

# block_hash = '000000000000000002b32e242989056214fef31c5aac08ae517840db3e3e7fd2'
# block_num = '341537'
# block = blockexplorer.get_block(block_hash)
def totalValue(xPuts):
	totalValue = 0
	for x in xPuts:
		totalValue += x.value
	return totalValue

def contains(address_string, array):
	for xPut in array:
		if address_string == xPut.address:
			return True
	return False

def createLeavingEdges(edge_factory, edges, address_string, inputs, outputs):
	total_output = totalValue(outputs)
	# print total_output
	for i in inputs:
		if address_string == i.address:
			value = i.value
			
			for o in outputs:
				received = o.value
				ratio = Decimal(received) / Decimal(total_output)
				weighted_received = ratio *  Decimal(value)
				e = edge_factory.NewEdge(address_string, o.address, weighted_received)
				edges.append(e)

def createIncomingEdges(edge_factory, edges, address_string, inputs, outputs):
	total_output = totalValue(outputs)
	for o in outputs:
		if address_string == o.address:
			received = o.value
			ratio = Decimal(received) / Decimal(total_output)
			for i in inputs:
				weighted_sent = ratio * Decimal(i.value)
				e = edge_factory.NewEdge(i.address, address_string, weighted_sent)
				edges.append(e)





class Edge: 
	def __init__(self, s, t, w, si, ti):
		self.source = s
		self.target = t
		self.weight = w
		self.source_index = si
		self.target_index = ti

	def __repr__(self):
		s = '[ \'' + self.source + '\', ' + '\'' + self.target + '\', ' + str(self.weight) + ']'
		
		return s

class EdgeFactory:
	def __init__(self):
		self.node_counter = 0
		self.node_index_map = {}

	def NewEdge(self, source, target, weight):
		self.node_index_map
		if source in self.node_index_map:
			source_index = self.node_index_map[source]
		else:
			self.node_index_map[source] = self.node_counter
			source_index = self.node_counter
			self.node_counter += 1

		if target in self.node_index_map:
			target_index = self.node_index_map[target]
		else:
			self.node_index_map[target] = self.node_counter
			target_index = self.node_counter
			self.node_counter += 1

		edge = Edge(source, target, weight, source_index, target_index)
		return edge

	def GetNodeIndexMap(self):
		return self.node_index_map




unexploredAddresses = []
exploredAddresses = []
edges = []
edge_factory = EdgeFactory()

address_string = '17bWK1kGySckEV7jpNBHUmHuX1UoHeHoAs'
address_object = blockexplorer.get_address(address_string)

# attributes = dir(address)
# print 'Address attributes:'
# for t in attributes:
# 	x = getattr(address,t)

# 	print '\t',t, '\t\t\t', x

# outputtemp = address_object.transactions[0].outputs[0]
# attributes = dir(outputtemp)
# print 'Output attributes:'
# for t in attributes:
# 	x = getattr(outputtemp,t)

# 	print '\t',t, '\t\t\t', x

i = 0
transactions = address_object.transactions
for t in transactions:
	inputs = t.inputs
	outputs = t.outputs
	createLeavingEdges(edge_factory, edges, address_string, inputs, outputs)
	createIncomingEdges(edge_factory, edges,address_string,inputs,outputs)
	

node_list_result = ''
node_map = edge_factory.GetNodeIndexMap()
node_list = node_map.items()
node_list = sorted(node_list, key=operator.itemgetter(1))
print node_list
for node in node_list:
	node_list_result += '{"name":"' + node[0] + '"},'
node_list_result = node_list_result[:-1]

link_list_result = ''



result = '{"nodes":[' + node_list_result + '],"links":[' + link_list_result + ']}'
print result

# for e in edges:
# 	print str(e) + ','



# {"nodes":[{"name":"Oil"},{"name":"Natural Gas"},{"name":"Coal"},{"name":"Fossil Fuels"},{"name":"Electricity"},{"name":"Energy"}],"links":[{"source":0,"target":3,"value":15},{"source":1,"target":3,"value":20},{"source":2,"target":3,"value":25},{"source":2,"target":4,"value":25},{"source":3,"target":5,"value":60},{"source":4,"target":5,"value":25},{"source":4,"target":5,"value":25},{"source":4,"target":4,"value":5.5}]}



# hash = '62e907b15cbf27d5425399ebf6f0fb50ebb88f18'
# print util.hash_to_address("00".decode('hex'), hash.decode('hex'))








# attributes = dir(block)
# print 'Block attributes:'
# for t in attributes:
# 	x = getattr(block,t)

# 	if t == 'transactions':
# 		print '\ttransactions: [array nigga]'
# 		continue
# 	print '\t',t, '\t\t\t', x


# print '\n', 'Transaction attributes'

# transactions = block.transactions
# trans = transactions[50]

# trans_attributes = dir(trans)
# for t in trans_attributes:
# 	x = getattr(trans,t)
# 	if t == 'inputs' or t == 'outputs':
# 		print '\t', t, '\t\t\t', 'array nigga'
# 		continue
# 	print '\t',t, '\t\t\t', x

# tx_val = get_transaction_amount(trans)

# print '\n', 'Input attributes'
# input = trans.inputs[0]

# input_attributes = dir(input)

# for t in input_attributes:
# 	x = getattr(input,t)
# 	print '\t',t, '\t\t\t', x

# print '# of outputs', len(trans.outputs)
# print '\n', 'Output attributes'
# output = trans.outputs[0]

# output_attributes = dir(output)

# for t in output_attributes:
# 	x = getattr(output,t)
# 	print '\t',t, '\t\t\t', x





