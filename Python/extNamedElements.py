import json
import re

class NamedElements:
    
	def __init__(self, owner):
		print("init NamedElements extension")
		self.owner = owner
		self.parent_storage = op.NAPs.storage

		try:
			self.named_operators = op.NAPs.storage["named_operators"]
		except KeyError:
			op.NAPs.storage.update({"named_operators":{}})
			self.named_operators = op.NAPs.storage["named_operators"]
		
		try:
			self.named_parameters = op.NAPs.storage["named_parameters"]
		except KeyError:
			op.NAPs.storage.update({"named_parameters":{}})
			self.named_parameters = op.NAPs.storage["named_parameters"]

		self.validName = r'^[A-z][A-z_0-9]*$'	# regex for testing op/par name validity
		self.namedOperatorsDAT = op("named_operators")
		self.namedParametersDAT = op("named_parameters")
	

	def InitNamedOperatorsDict(self):
		op.NAPs.storage["named_operators"].clear()
		self.namedOperatorsDAT.clear()
	
	def InitNamedParametersDict(self):
		op.NAPs.storage["named_parameters"].clear()
		self.namedParametersDAT.clear()
	
	def AddNamedOperator(self, args):
			# args is passed in from the popDialog function

			# operator is reference to operator object
		operator = args["details"]["operator"]
		name = args["enteredText"]

			# check if name already exists
		if name in self.named_operators:
			message = f'The name `{name}` already exists.'
			ui.messageBox("ERROR: Duplicate OP Names", message, buttons=["OK"])
			return -1

			# check if name is valid pattern
		if re.match(self.validName, name):
			# add to dict and update table for user viewability
			self.named_operators.update({name:operator})
			self.namedOperatorsDAT.appendRow([name, ""])
			return 0
		else:
			message = "OP names can only contain letters, numbers and underscores, and cannot start with a number.\nPlease enter a different name."
			ui.messageBox("ERROR: Invalid Operator Name",message, buttons=["OK"])
			return -1
		
	def DeleteNamedOperator(self, op_name):
		if op_name in self.named_operators:
			self.named_operators.pop(op_name)
			self.namedOperatorsDAT.deleteRow(op_name)
			return 0
		
		else:
			return -1
	

	def AddNamedParameter(self, args):
		parameter = args["details"]["parameter"]
		name = args["enteredText"]

		if name in self.named_parameters:
			message = f'The name `{name}` already exists.'
			ui.messageBox("ERROR: Duplicate Par Names", message, buttons=["OK"])
			return -1

		if re.match(self.validName, name):
			self.named_parameters.update({name:parameter})
			self.namedParametersDAT.appendRow([name, ""])
			return 0
		else:
			message = "Par names can only contain letters, numbers and underscores, and cannot start with a number.\nPlease enter a different name."
			ui.messageBox("ERROR: Invalid Parameter Name",message, buttons=["OK"])
			return -1

		
