import uuid
import re

class Permission:

	def __init__(self, user, config):
		self._key = None
		self.config = config
		self.user = user
		self.userConfig = self.config.get(self.user)
		if self.userConfig:
			self.scopes = self.ingestScopes(self.config[self.user].get('scopes'))
			self.exclusions = self.ingestExclusions(self.config[self.user].get('exclusions'))
			self.createKey()
		else:
			del self
			raise Exception(f'User does not exist in the configuration.')
			

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
		if 'permissions' not in _scopes:
			_scopes.append('permissions')
		return [re.compile(scope) for scope in _scopes]
	
	def ingestExclusions(self, _exclusions):
		if _exclusions:
			return [re.compile(exclusion) for exclusion in _exclusions]
		else:
			return None

	def validatePermission(self, givenScope):
		permitted = False
		for scope in self.scopes:
			if re.match(scope, givenScope):
				permitted = True
		if self.exclusions:
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

