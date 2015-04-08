from blockchain import blockexplorer
import requests
import datetime

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

class Edge: 
	def __init__(self):
		self.source = ''
		self.target = ''
		self.weight = 0



unexploredAddresses = []
exploredAddresses = []


address = '17bWK1kGySckEV7jpNBHUmHuX1UoHeHoAs'
addrObj = blockexplorer.get_address(address)

attributes = dir(addrObj)
print 'Address attributes:'
for t in attributes:
	x = getattr(addrObj,t)

	print '\t',t, '\t\t\t', x

print 'transaction count:', len(addrObj.transactions)















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





