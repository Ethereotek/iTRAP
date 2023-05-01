import re
# param_pattern = re.compile("\\w+(?=>)")

class TrieNode:
	def __init__(self):
		self.name = 'root'
		self.children = {}
		self.handler = None
		self.handlers = None
		self.param_name = None
		self.end = False
	
class Trie:
	param_pattern = re.compile("\\w+(?=>)")

	def __init__(self):
		self.root = TrieNode()

	def insert(self, path: str, handlers:dict) -> None:
		node = self.root
		path = path.strip('/')

		for segment in path.split('/'):
			# check if the segment is a parameter
			param = re.findall(self.param_pattern, segment)
			if param:
				name = param[0]					# 0th index is the matched string, i.e. name of parameter
				if name not in node.children:	# if it's not a child, 
					node.param_name = name		# add it as the parameter of the current node
					node.children.update({name:TrieNode()})	# then add it as a child with a new TrieNode

				node = node.children[name]		# go to next Node, the one that was just created
				node.name = name
			else:
					# if segment is not a child of current node, 
					# 	add it as a child, then switch to that node
				if segment not in node.children:	
					node.children.update({segment: TrieNode()})

				node = node.children[segment]
				node.name = segment
		
			# after all segments have been cycled through, add handler
		node.handlers = handlers

	def find(self, path: str, method:str):
		node = self.root
		path = path.strip('/')
		params = {}

		segments = path.split('/')
		numSegments = len(segments)

		for segment in path.split('/'):
			# print('find: node name = ', node.name)
			if numSegments > 0:
				if node.param_name:
					params.update({node.param_name:segment})
					node = node.children[node.param_name]
					
				elif segment in node.children:
					node = node.children[segment]
			numSegments -= 1
		return node.handlers[method], params


trie = Trie()
def TestHandler(func):
	def wrapper(*args, **kwargs):
		print("doing stuff all functions need")
		func(*args, **kwargs)
		
	return wrapper

@TestHandler
def handleAppPower(*args, **kwargs):
	method = kwargs['method']
	data = kwargs['data']

	def get():
		print('getting app power')
	
	def put():
		print('putting app power')
	
	if method == 'GET':
		get()
	elif method == 'PUT':
		put()

def handleOp(*args, **kwargs):
	method = kwargs['method'],
	params = args[0]

	print("handling ops")
	print(params)

def handleOpPar(*args, **kwargs):
	method = kwargs['method'],
	params = args[0]

	print("handling op par")
	print(params)
	




def handleUser(*args):
	params = args[0]
	print(params)
	print('user')

# trie.insert('/api/v1/users/<user>', handleUser)
# trie.insert('/api/v1/app/power', handleAppPower)
# trie.insert('/api/v1/op/<id>', handleOp)

def getOpPar():
	print('get op par')
def putOpPar():
	print('put op par')

trie.insert('/api/v1/op/<id>/par/<name>', {'GET':getOpPar,'PUT':putOpPar})

func, params = trie.find('api/v1/op/23/par/radius', 'PUT')
print(func, params)
func()
#func(params,data = {}, method='GET')

