from blockchain import blockexplorer
from decimal import *
import requests
import operator
import datetime

print '\n\n\n\n\n\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'

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

# def explore_address(address):
# 	print 'TODO'

# Gets $USD of 1 bitcoin
# def get_conversion_rate():
# 	timestamp = datetime.datetime.now()

# 	# This url returns the value of bitcoin for the given amount of USD
# 	USD_URL = 'https://blockchain.info/tobtc'
# 	payload = {'currency': 'USD', 'value': '100'}
# 	r = requests.get(USD_URL, params=payload)

# 	x = float(r.text)
# 	dollars = 100.0 / x
# 	print dollars
# 	return (timestamp, dollars)

def totalValue(xPuts):
	totalValue = 0
	for x in xPuts:
		totalValue += x.value
	return totalValue

# def contains(address_string, array):
# 	for xPut in array:
# 		if address_string == xPut.address:
# 			return True
# 	return False

def createLeavingEdges(exploredAddresses, unexploredAddresses, edge_factory, edges, address_string, inputs, outputs):
	total_output = totalValue(outputs)
	# print total_output
	for i in inputs:
		if address_string == i.address:
			value = i.value
			
			for o in outputs:
				if o.address in exploredAddresses:
					continue
				received = o.value
				ratio = Decimal(received) / Decimal(total_output)
				weighted_sent = ratio *  Decimal(value)
				if o.address in unexploredAddresses:
					unexploredAddresses[o.address] += weighted_sent
				else:
					unexploredAddresses[o.address] = weighted_sent
				e = edge_factory.NewEdge(address_string, o.address, weighted_sent)
				edges.append(e)

def createIncomingEdges(exploredAddresses, unexploredAddresses, edge_factory, edges, address_string, inputs, outputs):
	total_output = totalValue(outputs)
	for o in outputs:
		if address_string == o.address:
			received = o.value
			ratio = Decimal(received) / Decimal(total_output)
			for i in inputs:
				if i.address in exploredAddresses:
					continue
				weighted_received = ratio * Decimal(i.value)
				if i.address in unexploredAddresses:
					unexploredAddresses[i.address] += weighted_received
				else:
					unexploredAddresses[i.address] = weighted_received
				e = edge_factory.NewEdge(i.address, address_string, weighted_received)
				edges.append(e)

def popUnexploredAddress(unexploredAddresses):
	tuples = unexploredAddresses.items()
	address,weight = tuples[0]

	for (a, w) in tuples:
		if w > weight:
			address,weight = a,w

	unexploredAddresses.pop(address)
	return address

unexploredAddresses = {}
exploredAddresses = set()
edges = []
edge_factory = EdgeFactory()



root_address = '17bWK1kGySckEV7jpNBHUmHuX1UoHeHoAs'
unexploredAddresses[root_address] = 1

# Explore an address, create edges in/out of this address
for i in range(3):
	address_string = popUnexploredAddress(unexploredAddresses)

	address_object = blockexplorer.get_address(address_string)

	transactions = address_object.transactions
	for t in transactions:
		inputs = t.inputs
		outputs = t.outputs
		createLeavingEdges(exploredAddresses, unexploredAddresses, edge_factory, edges, address_string, inputs, outputs)
		createIncomingEdges(exploredAddresses, unexploredAddresses, edge_factory, edges,address_string,inputs,outputs)

	exploredAddresses.add(address_string)

	


# Create input string for Sankey diagram given edges and edge_factory
node_list_result = ''
node_map = edge_factory.GetNodeIndexMap()
node_list = node_map.items()
node_list = sorted(node_list, key=operator.itemgetter(1))
for node in node_list:
	node_list_result += '{"name":"' + node[0] + '"},'
node_list_result = node_list_result[:-1]

link_list_result = ''
for e in edges:
	link_list_result += '{"source":'+ str(e.source_index) + ',"target":' + str(e.target_index) + ',"value":' + str(e.weight) + '},'
link_list_result = link_list_result[:-1]

# Example of what input string needs to look like
# {"nodes":[{"name":"Oil"},{"name":"Natural Gas"},{"name":"Coal"},{"name":"Fossil Fuels"},{"name":"Electricity"},{"name":"Energy"}],"links":[{"source":0,"target":3,"value":15},{"source":1,"target":3,"value":20},{"source":2,"target":3,"value":25},{"source":2,"target":4,"value":25},{"source":3,"target":5,"value":60},{"source":4,"target":5,"value":25},{"source":4,"target":5,"value":25},{"source":4,"target":4,"value":5.5}]}
result = '{"nodes":[' + node_list_result + '],"links":[' + link_list_result + ']}'
print result




# print '\n', 'Input attributes'
# input = trans.inputs[0]

# input_attributes = dir(input)

# for t in input_attributes:
# 	x = getattr(input,t)
# 	print '\t',t, '\t\t\t', x







