import re

class TrieNode:
	def __init__(self):
		self.name = 'root'
		self.children = {}
		self.handlers = None
		self.param_name = None
		self.end = False
		self.scope = 'root'
	
class Trie:
	param_pattern = re.compile("\\w+(?=>)")

	def __init__(self):
		self.root = TrieNode()

	def insert(self, path: str, handlers: dict, scope: str) -> None:
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
				if segment not in node.children:	
					node.children.update({segment: TrieNode()})

				node = node.children[segment]
				node.name = segment
		
			# after all segments have been cycled through, add handlers
		node.handlers = handlers
		node.scope = scope

	def find(self, path: str):
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
				else:
					return None, {}
			
			numSegments -= 1


		# return node.handlers.get(method), params, node.scope
		return node, params



