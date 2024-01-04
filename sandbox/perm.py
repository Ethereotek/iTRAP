import uuid
import re
config = {
	"admin": {
		"scopes": [
			"app.*",
			"project.*",
			"namedOp.*",
			"monitors.*",
			"project.*",
			"ui.*",
			"namedPars.*"
		],
		"exclusions":[
			
		],
		"key": "ec3c304e-e937-11ed-8bc6-9cfce837ddb7"
	}
}


class Permission:

	def __init__(self, user, config):
		self._key = None
		self.config = config
		self.user = user
		self.scopes = self.ingestScopes(self.config[self.user].get('scopes'))
		self.exclusions = self.ingestExclusions(self.config[self.user].get('exclusions'))
		self.createKey()

	@property
	def key(self):
		return (str(self._key))

	def createKey(self):
		self._key = uuid.uuid1()

	def addScope(self, _scope):
		pass

	def removeScope(self, _scope):
		pass

	def ingestScopes(self, _scopes):
		return [re.compile(scope) for scope in _scopes]
	
	def ingestExclusions(self, _exclusions):
		return [re.compile(exclusion) for exclusion in _exclusions]

	def validatePermission(self, givenScope):
		permitted = False
		for scope in self.scopes:
			if re.match(scope, givenScope):
				permitted = True
		
		for exclusion in self.exclusions:
			if re.match(exclusion, givenScope):
				permitted = False
		''' GPT: The validatePermission() method currently returns a boolean value 
		indicating whether the given scope is permitted or not. 
		Consider modifying the method to provide more detailed feedback to the user, 
		such as a message indicating which scope was excluded and why.

		ME: so maybe use a dict, and if not permitted, message can be sent to user... maybe
		'''
		return permitted


permission = Permission('admin', config)

permitted = permission.validatePermission('app.architecture.put')
print(permitted)
