import json
from functools import wraps
import copy

schemas = mod('schemas').schemas
ttree = mod('ttree_builder')
permissions = mod('Permissions')
request_validation = mod('request_validation')
butils = mod('butils')

permissions_config_dat = op('permissions_config')


class ITRAP():
	routing_table = {}
	routing_tree = ttree.Trie()

	def __init__(self, thisComp):
		self.thisComp = thisComp
		self.itrap_port = thisComp.par.Port
		self.ip_address = thisComp.par.Ipaddress

		if not self.thisComp.storage.get('Permissions'):
			self.thisComp.store('Permissions', {'keys': {}, 'users': {}})
		print(thisComp)

		self.routing_table = {
			"/api/banana/permissions": {'handlers': {'GET': self.getPermissions}, 'scope': 'permissions'},
			"/api/banana/app/architecture": {'handlers': {'GET': self.getAppArchitecture}, 'scope': 'app.architecture'},
			"/api/banana/app/build": {'handlers': {'GET': self.getAppBuild}, 'scope': 'app.build'},
			"/api/banana/app/launchTime": {'handlers': {'GET': self.getAppLaunchTime}, 'scope': 'app.launchTime'},
			"/api/banana/app/startTimestamp": {'handlers': {'GET': self.getAppStartTimestamp}, 'scope': 'app.startTimestamp'},
			"/api/banana/app/osName": {'handlers': {'GET': self.getAppOSName}, 'scope': 'app.osName'},
			"/api/banana/app/power": {'handlers': {'GET': self.getAppPower, 'PUT': self.putAppPower}, 'scope': 'app.power'},
			"/api/banana/app/product": {'handlers': {'GET': self.getAppProduct}, 'scope': 'app.product'},
			"/api/banana/app/version": {'handlers': {'GET': self.getAppVersion}, 'scope': 'app.version'},
			"/api/banana/app/play": {'handlers': {'GET': self.getAppPlay, 'PUT': self.putAppPlay}, 'scope': 'app.play'},
			"/api/banana/project/name": {'handlers': {'GET': self.getProjectName}, 'scope': 'project.name'},
			"/api/banana/project/saveVersion": {'handlers': {'GET': self.getProjectSaveVersion}, 'scope': 'project.saveVersion'},
			"/api/banana/project/saveBuild": {'handlers': {'GET': self.getProjectSaveBuild}, 'scope': 'project.saveBuild'},
			"/api/banana/project/saveTime": {'handlers': {'GET': self.getProjectSaveTime}, 'scope': 'project.saveTime'},
			"/api/banana/project/saveOSName": {'handlers': {'GET': self.getProjectSaveOSName}, 'scope': 'project.saveOSName'},
			"/api/banana/project/saveOSVersion": {'handlers': {'GET': self.getProjectSaveOSVersion}, 'scope': 'project.saveOSVersion'},
			"/api/banana/project/paths": {'handlers': {'GET': self.getProjectPaths, 'PUT': self.putProjectPaths}, 'scope': 'project.paths'},
			"/api/banana/project/paths/path/<name>": {'handlers': {'GET': self.getProjectPath, 'PUT': self.putProjectPath}, 'scope': 'project.paths'},
			"/api/banana/project/paths/new": {'handlers': {'POST': self.postProjectPath}, 'scope': 'project.paths'},
			"/api/banana/project/cookRate": {'handlers': {'GET': self.getProjectCookRate, 'PUT': self.putProjectCookRate}, 'scope': 'project.cookRate'},
			"/api/banana/project/realTime": {'handlers': {'GET': self.getProjectRealTime, 'PUT': self.putProjectRealTime}, 'scope': 'project.'},
			"/api/banana/project/performOnStart": {'handlers': {'GET': self.getProjectPerformOnStart, 'PUT': self.putProjectPerformOnStart}, 'scope': 'project.performOnStart'},
			"/api/banana/project/load": {'handlers': {'POST': self.postProjectLoad}, 'scope': 'project.load'},
			"/api/banana/project/save": {'handlers': {'POST': self.postProjectSave}, 'scope': 'project.save'},
			"/api/banana/project/quit": {'handlers': {'POST': self.postProjectQuit}, 'scope': 'project.quit'},
			"/api/banana/sysinfo/numCPUs": {'handlers': {'GET': self.getSysInfoNumCpus}, 'scope': 'sysinfo.numCPUs'},
			"/api/banana/sysinfo/ram": {'handlers': {'GET': self.getSysInfoRAM}, 'scope': 'sysinfo.ram'},
			"/api/banana/ui/masterVolume": {'handlers': {'GET': self.getUIMasterVolume, 'PUT': self.putUIMasterVolume}, 'scope': 'ui.masterVolume'},
			"/api/banana/monitors": {'handlers': {'GET': self.getMonitors}, 'scope': 'monitors.'},
			"/api/banana/monitors/monitor/<mon>": {'handlers': {'GET': self.getMonitor}, 'scope': 'monitors.monitor'},
			"/api/banana/monitors/monitor/<mon>/<attribute>": {'handlers': {'GET': self.getMonitorAttribute}, 'scope': 'monitors.monitor'},
			"/api/banana/monitors/refresh": {'handlers': {'POST': self.postMonitorsRefresh}, 'scope': 'monitors.refresh'},
			"/api/banana/op": {'handlers': {'GET': self.getOp, 'POST': self.postOp, 'DELETE': self.deleteOp}, 'scope': 'ops'},
			"/api/banana/op/attributes/<attribute>": {'handlers': {'GET': self.getOpAttribute, 'PUT': self.putOpAttribute}, 'scope': 'ops.attribute'},
			"/api/banana/op/opIdMap": {'handlers': {'GET': self.getOpIdMap}, 'scope': 'ops.opIdMap'},
			"/api/banana/op/id": {'handlers': {'GET': self.getOpID}, 'scope': 'ops.id'},
			"/api/banana/op/cookMetrics": {'handlers': {}, 'scope': 'ops.cook'},
			"/api/banana/op/id/<op-id>/par/<par-name>": {'handlers': {'GET': self.getOpPar}, 'scope': 'ops.par'},
			"/api/banana/op/id/<id>/par/<par>/val/<val>": {'handlers': {'PUT': self.putOpPar}, 'scope': 'ops.par.val'},
			"/api/banana/op/name": {'handlers': {'GET': self.getOpName, 'PUT': self.putOpName}, 'scope': 'ops.name'},
			"/api/banana/op/storage": {'handlers': {'GET': self.getOpStorage}, 'scope': 'ops.storage'},
			"/api/banana/op/tags": {'handlers': {'GET': self.getOpTags, 'POST': self.postOpTags, 'DELETE': self.deleteOpTags}, 'scope': 'ops.tags'},
			"/api/banana/op/par": {'handlers': {'GET': self.getOpPar, 'PUT': self.putOpPar}, 'scope': 'ops.par'},
			"/api/banana/namedOps": {'handlers': {'GET': self.getNamedOps}, 'scope': 'namedOps'},
			"/api/banana/namedOps/op/<name>": {'handlers': {'GET': self.getNamedOp}, 'scope': 'namedOps'},
			"/api/banana/namedOps/op/<name>/attribute/<attribute>": {'handlers': {'GET': self.getNamedOpAttribute, 'PUT': self.putNamedOpAttribute}, 'scope': 'namedOps.attribute'},
			"/api/banana/namedOps/op/<name>/par/<par>": {'handlers': {'GET': self.getNamedOpPar, 'PUT': self.putNamedOpPar}, 'scope': 'namedOps.par'},
			"/api/banana/namedPars": {'handlers': {'GET': self.getNamedPars}, 'scope': 'namedPars'},
			"/api/banana/namedPars/par/<name>": {'handlers': {'GET': self.getNamedPar, 'PUT': self.putNamedPar}, 'scope': 'namedPars'}

		}

		for key, val in self.routing_table.items():
			handlers = val.get('handlers')
			scope = val.get('scope')
			self.routing_tree.insert(key, handlers, scope)

# --------------------------------------------------------------#
# --------------------------------------------------------------#
# --------------------------------------------------------------#
	def getPermission(self):

		self.token = self.request.get('Authorization')

		# if there is no token
		if not self.token:
			self.formatResponse(401, 'Not Authorized', {'error': 'no token'})
			return False

		# if the token can't be unpacked
		else:
			try:
				self.token = self.token.split(' ')[1]

			except:
				self.formatResponse(400, 'Bad Format', {})
				return False

		permission = self.thisComp.storage['Permissions']['keys'].get(
			self.token)
		return permission

	def getTrieNode(self):
		pass

	def handleBanana(self):
		pass

	def HandleRequest(self, request, response):
		self.request = request
		self.response = response
		self.parameters = request['pars']
		uri = request['uri']
		if uri.endswith('/'):
			uri = uri[:-1]
		print(uri)
		method = request['method']

		self.response['content-type'] = 'application/json'
		self.rel_prefix = f'http://{self.ip_address}:{self.itrap_port}/'

		self.permission = self.getPermission()
		if not self.permission:
			self.formatResponse(401, 'Not Authorized', {
								'error': 'no permissions found'})
			return self.response

		# handler, params, scope = self.routing_tree.find(uri, method)
		node, params = self.routing_tree.find(uri)
		handler = node.handlers.get(method)
		scope = node.scope
		if not handler:
			allow = ','.join(node.handlers.keys())
			response['Allow'] = allow
			self.formatResponse(405, 'Method Not Allowed', {})
			return self.response

		# check that scope is allowed in apiKey's permission
		scope += ('.' + method.lower())
		permitted = self.permission.validatePermission(scope)

		if not permitted:
			self.formatResponse(401, 'Not Authorized', {
								'error': 'not permitted'})
			return self.response

		# add the parameters collected from the URL parsing to self.parameters
		if params:
			self.parameters.update(params)

		if uri.split('/')[2] == 'monkey':
			handler(self)
		else:
			handler()
		return self.response

	def format500(self, data=None, error='unknown'):
		if not data:
			data = {
				'error': {'message': f'Server encountered an exception while encoding return data.',
						  'exception': error}
			}
		self.response['statusCode'] = 500
		self.response['statusReason'] = 'Internal Server Error'
		self.response['data'] = data

	def formatResponse(self, code, reason, data={}):
		try:
			data = json.dumps(data)
		except Exception as e:
			self.format500(error=str(e))
		finally:
			self.response["statusCode"] = code
			self.response["statusReason"] = reason
			self.response["data"] = data

	def InsertRoute(self, url: str, handlers: dict, scope: str):
		self.url = url
		url = '/api/monkey' + url
		self.routing_tree.insert(url, handlers, scope)

	def CreateKey(self, user):
		permissions_config = json.loads(permissions_config_dat.text)
		# create a permission object, which has a key
		# assign key to the user, update configuration, and store key:permission in parent dict
		permission = permissions.Permission(user, permissions_config)
		key = permission.key
		permissions_config[user].update({'key': permission.key})
		permissions_config_dat.text = json.dumps(permissions_config)
		permissions_dict = self.thisComp.storage["Permissions"]
		if permissions_dict["users"].get(user):
			current_key = permissions_dict["users"].get(user)
			permissions_dict["keys"].pop(current_key)
		permissions_dict['keys'].update({key: permission})
		permissions_dict['users'].update({user: key})

	def quit(self):
		project.quit(force=True)

	def formatMissingParamMessage(self, param):
		data = {
			'error': {
				'message': f'KeyError: Missing required parameter {param}.'
			}
		}
		self.formatResponse(400, 'Bad Request', data)
		return -1

	def formatTypeErrorMessage(self, param, _type):
		data = {
			'error': {
				'message': f'TypeError: "{param}" must be type {_type}'
			}
		}
		self.formatResponse(400, 'Bad Request', data)
		return -1

# --------------------------------------------------------------#
# -------------------------- WRAPPERS --------------------------#
# --------------------------------------------------------------#
	'''
	This is a bit confusing and needs to be fixed, but:
		if the parameters are in the body, use handler(), otherwise use handleGet()
		The handler() method assumes the data is a parameters object
		It has the logic set up to unpack 'params' from the data dictionary, but doesn't actually use that
		In this logic, if data.get('params') returns None, it uses self.parameters
		In this way, we should be able to combine both handlers into one,
		The spec needs to be updated to require that the parameters be the value to a property called "params"
	'''
	def handler(thisSchema):
		def decorator(func):
			@wraps(func)
			def wrapper(self, *args, **kwargs):
				data = None
				try:
					data = json.loads(self.request['data'])
				except:
					self.formatResponse(400, 'Bad Request', {
										'error': 'Bad JSON formatting.'})
					return
				params = data.get('params')
				schema = thisSchema
				if not params:
					print('no params')
					params = self.parameters
				hasParams, validTypes = request_validation.validateParametersDict(
					data, schema)
				if hasParams and validTypes:
					# this will require some rework, but can pass deserialized data through params
					func(self, data, *args, **kwargs)
				else:
					self.formatResponse(400, 'Bad Request', {
										"error": "Missing params, or wrong type."})
			return wrapper
		return decorator

	def handleGet(thisSchema):
		def decorator(func):
			@wraps(func)
			def wrapper(self, *args, **kwargs):
				params = self.parameters
				schema = thisSchema
				hasParams, validTypes = request_validation.validateParametersDict(
					params, schema)
				# print("params -> ", params)
				# print("schema -> ", schema)
				# print("hasParams -> ", hasParams)
				# print("validTypes -> ", validTypes)
				if hasParams and validTypes:
					func(self, *args, **kwargs)
				else:

					self.formatResponse(400, 'Bad Request', {})
			return wrapper
		return decorator

# --------------------------------------------------------#
# -------------------- BEGIN HANDLERS --------------------#
# --------------------------------------------------------#

# -----------------------------------------------------#
# -------------------- PERMISSIONS --------------------#
# -----------------------------------------------------#

	def getPermissions(self):
		permissionObject = self.thisComp.storage['Permissions']['keys'].get(
			self.token)
		scopes = [scope.pattern for scope in permissionObject.scopes]
		exclusions = permissionObject.exclusions
		user = permissionObject.user
		data = {
			'name': f'{user} Permissions',
			'scope': 'permissions',
			'description': '',
			'data': {
					'scopes': scopes,
					'exclusions': exclusions
			}
		}
		self.formatResponse(200, 'OK', data)

# -----------------------------------------------------#
# -------------------- APPLICATION --------------------#
# -----------------------------------------------------#

	def getAppArchitecture(self):
		data = {
			'name': 'Application Architecture',
			'scope': 'app.architecture',
			'description': 'The architecture of the compile. Generally 32 or 64 bit.',
			'built-in': True,
			'data': {
					'value': app.architecture,
					'type': 'int'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/app/architecture'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppBuild(self):
		data = {
			'name': 'Application Build',
			'scope': 'app.build',
			'description': 'Application build number.',
			'built-in': True,
			'data': {
					'value': app.build,
					'type': 'str'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/app/build'
				},
				{
					'rel': 'app.product',
					'href': self.rel_prefix + 'api/banana/app/product'
				}, {
					'rel': 'app.version',
					'href': self.rel_prefix + 'api/banana/app/version'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppLaunchTime(self):
		data = {
			'name': 'Application Launch Time',
			'scope': 'app.launchTime',
			'description': 'Total time required to launch and begin playing the toe file, measured in seconds.',
			'built-in': True,
			'data': {'value': app.launchTime,
					 'type': 'float'},
			'links': [{'rel': 'self',
					   'href': self.rel_prefix + 'api/banana/app/launchTime'},
					  {'rel': 'app.startTimestamp',
					   'href': self.rel_prefix + 'api/banana/app/startTimestamp'}]
		}
		self.formatResponse(200, 'OK', data)

	def getAppStartTimestamp(self):
		timestamp = op('records')['startTimestamp', 'value'].val
		data = {
			'name': 'Application Start Time',
			'scope': 'app.startTimestamp',
			'description': 'UNIX timestamp recorded when the application starts.',
			'built-in': False,
			'data': {
					'value': float(timestamp),
					'type': 'float'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/app/startTimestamp'
				}, {
					'rel': 'app.launchTime',
					'href': self.rel_prefix + 'api/banana/app/launchTime'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppOSName(self):
		data = {
			'name': 'Application OS Name',
			'scope': 'app.osName',
			'description': 'The operating system name.',
			'built-in': True,
			'data': {
					'value': app.osName,
					'type': 'str'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/app/osName'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppPower(self):
		data = {
			'name': 'Application Power State',
			'scope': 'app.power',
			'description': 'Processing state of the application. This has a greater effect than simply pausing or stopping the playbar.',
			'data': {
					'value': app.power,
					'type': 'bool'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/app/power'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	@handler(schemas['put_app_power'])
	def putAppPower(self, data):
		power = data["state"]
		app.power = power
		data = {
			'success': {
				'name': 'Application Power',
				'scope': 'app.power',
						'data': {
							'value': app.power,
							'type': 'bool'
						}
			}
		}
		self.formatResponse(200, 'OK', data)

	def getAppProduct(self):
		data = {
			'name': 'Application Product',
			'scope': 'app.product',
			'description': 'Type of executable the project is running under.',
			'built-in': True,
			'data': {
					'value': app.product,
					'type': 'str'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/app/product'
				}, {
					'rel': 'app.version',
					'href': self.rel_prefix + 'api/banana/app/version'
				},
				{
					'rel': 'app.build',
					'href': self.rel_prefix + 'api/banana/app/build'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppVersion(self):
		data = {
			'name': 'Application Version',
			'scope': 'app.version',
			'description': 'Application version number.',
			'built-in': True,
			'data': {
					'value': app.version,
					'type': 'str'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/app/version'
				}, {
					'rel': 'app.product',
					'href': self.rel_prefix + 'api/banana/app/product'
				},
				{
					'rel': 'app.build',
					'href': self.rel_prefix + 'api/banana/app/build'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppPlay(self):
		data = {
			'name': 'Application Transport State',
			'scope': 'app.play',
			'description': 'Indicates whether the application is playing or stopped.',
			'built-in': False,
			'data': {
					'value': op('/local/time').par.play.val,
					'type': 'integer'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/app.play'
				}
			]
		}

		self.formatResponse(200, 'OK', data)

	@handler(schemas['put_app_play'])
	def putAppPlay(self, data):
		play = data['play']
		op("/local/time").par.play = play
		data = {
			'sucess': {
				'name': 'Application Transport State',
				'scope': 'custom.app.play',
						'description': 'Indicates whether the application is playing or stopped.',
						'data': {
							'value': op("/local/time").par.play.val,
							'type': 'int'
						}
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/app.play'
				}
			]
		}

		self.formatResponse(200, 'OK', data)

# -------------------------------------------------#
# -------------------- PROJECT --------------------#
# -------------------------------------------------#
	def getProjectName(self):
		data = {
			'name': 'Project Name',
			'scope': 'project.name',
			'description': 'The filename under which the project is saved.',
			'built-in': True,
			'data': {'value': project.name,
					 'type': 'str'},
			'links': [{'rel': 'self',
					   'href': self.rel_prefix + 'api/banana/project/name'}]
		}
		self.formatResponse(200, 'OK', data)

	def getProjectPaths(self):
		data = {
			'name': 'Project Paths',
			'scope': 'project.paths',
			'description': 'A dictionary which can be used to define URL-syntax path prefixes, enabling you to move your media to different locations easily.',
			'built-in': True,
			'data': {'value': project.paths,
					 'type': 'dict'}
		}
		self.formatResponse(200, "OK", data)

	@handleGet(schemas['get_project_path'])
	def getProjectPath(self):
		name = self.parameters.get('name')
		path = project.paths.get(name)
		if path:
			data = {
				'name': f'Project Path: {name}',
				'scope': 'project.paths',
				'description': '',
				'data': {
						'value': path,
						'type': 'path'
				},
				'links': []
			}
			self.formatResponse(200, 'OK', data)
		else:
			self.formatResponse(404, 'Resource Not Found', {})

	@handler(schemas['post_project_path'])
	def postProjectPath(self):
		params = self.parameters
		name = params.get('name')
		path = params.get('path')

		if name in project.paths.keys():
			data = {
				'conflict': f'The named path {name} already exists. Use PUT to change it or choose a different name.'
			}
			self.formatResponse(409, 'Conflict')
		else:
			project.paths[name] = path
			data = {
				'success': {
					'name': 'Project Path',
					'scope': 'project.paths',
							'description': '',
							'built-in': True,
							'data': {'value': {name: path},
									 'type': 'dict'}
				}
			}
			self.formatResponse(201, 'Created', data)

	@handleGet(schemas['put_project_path'])
	def putProjectPath(self):
		name = self.parameters.get('name')
		path = self.parameters.get('path')
		currentPath = project.paths.get(name)
		if currentPath:
			project.paths[name] = path
			data = {
				'name': f'Project Path {name}',
				'scope': 'project.paths',
				'data': {'value': project.paths.get(name),
						 'type': 'str'}
			}
			self.formatResponse(200, 'OK', data)
		else:
			data = {'error': f'{name} is not in project paths.'}
			self.formatResponse(404, 'Resource Not Found', data)

	def putProjectPaths(self):
		pass

	def getProjectCookRate(self):
		data = {
			'name': 'Project Cook Rate',
			'scope': 'project.cookRate',
			'description': 'The maximum number of frames processed each second.',
			'built-in': True,
			'data': {'value': project.cookRate,
					 'type': 'float'},
			'links': [{'rel': 'self',
					   'href': self.rel_prefix + 'api/banana/project/cookRate'}]
		}
		self.formatResponse(200, "OK", data)

	@handler(schemas['put_project_cookRate'])
	def putProjectCookRate(self, data):
		rate = data['rate']
		project.cookRate = rate
		data = {
			'success': {
				'name': 'Project Cook Rate',
				'scope': 'project.cookRate',
				'data': {'value': project.cookRate,
						 'type': 'float'}
			},
			'links': [{'rel': 'self',
					   'href': self.rel_prefix + 'api/banana/project/cookRate'}]
		}
		self.formatResponse(200, 'OK', data)

	def getProjectSaveVersion(self):
		data = {
			'name': 'Project Save Version',
			'scope': 'project.saveVersion',
			'description': 'The App version number when the project was last saved.',
			'built-in': True,
			'data': {'value': project.saveVersion,
					 'type': 'str'},
			'links': [{'rel': 'self',
					   'href': self.rel_prefix + 'api/banana/project/saveVersion'},
					  {'rel': 'Application Version',
					   'href': self.rel_prefix + 'api/banana/app/version'}]
		}
		self.formatResponse(200, 'OK', data)

	def getProjectSaveBuild(self):
		data = {
			'name': 'Project Save Build',
			'scope': 'project.saveBuild',
			'description': 'The App build number when the project was last saved.',
			'built-in': True,
			'data': {
					'value': project.saveBuild,
					'type': 'str'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/project/saveBuild'
				}, {
					'rel': 'Application Version',
					'href': self.rel_prefix + 'api/banana/app/build'
				}
			]
		}

		self.formatResponse(200, 'OK', data)

	def getProjectSaveTime(self):
		data = {
			'name': 'Project Save Time',
			'scope': 'project.saveTime',
			'description': 'The datetime formatted timestamp when the project was last saved.',
			'built-in': True,
			'data': {
					'value': project.saveTime,
					'type': 'datetime'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/project/saveTime'
				}
			]
		}

		self.formatResponse(200, 'OK', data)

	def getProjectSaveOSName(self):
		data = {
			'name': 'Project Save OS Name',
			'scope': 'project.saveOSName',
			'description': 'The App operating system name when the project was last saved.',
			'built-in': True,
			'data': {
					'value': project.saveOSName,
					'type': 'str'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/project/saveOSName'
				},
				{
					'rel': 'app.osName',
					'href': self.rel_prefix + 'api/banana/app/osName'
				},
				{
					'rel': 'project.saveOSVersion',
					'href': self.rel_prefix + 'api/banana/project/saveOSVersion'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getProjectSaveOSVersion(self):
		data = {
			'name': 'Project Save OS Version',
			'scope': 'project.saveOSVersion',
			'description': 'The App operating system version when the project was last saved.',
			'built-in': True,
			'data': {
					'value': project.saveOSVersion,
					'type': 'str'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/project/saveOSVersion'
				},
				{
					'rel': 'project.saveOSName',
					'href': self.rel_prefix + 'api/banana/project/saveOSName'
				},
				{
					'rel': 'app.osName',
					'href': self.rel_prefix + 'api/banana/app/osName'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getProjectRealTime(self):
		data = {
			'name': 'Project Real Time',
			'scope': 'project.realTime',
			'description': 'Realtime cooking state. When True, frames may be skipped in order to maintain the cookRate.',
			'built-in': True,
			'data': {
					'value': project.realTime,
					'type': 'bool'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/project/realTime'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	@handler(schemas['put_project_realTime'])
	def putProjectRealTime(self, data):
		realTime = data['realTime']

		project.realTime = realTime
		data = {
			'success': {
				'name': 'Project Real Time',
				'scope': 'project.realTime',
				'data': {
						'value': project.realTime,
						'type': 'bool'
				}
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/project/realTime'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getProjectPerformOnStart(self):
		data = {
			'name': 'Project Perform on Start',
			'scope': 'project.performOnStart',
			'description': 'If True, project starts in perform mode.',
			'built-in': True,
			'data': {
					'value': project.performOnStart,
					'type': 'bool'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/project/performOnStart'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	@handler(schemas['put_project_performOnStart'])
	def putProjectPerformOnStart(self, data):
		performOnStart = data['performOnStart']

		project.performOnStart = performOnStart
		data = {
			'success': {
				'name': 'Project Perform on Start',
				'scope': 'project.performOnStart',
				'data': {
					'value': project.performOnStart,
					'type': 'bool'
				}
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/project/performOnStart'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	@handler(schemas['post_project_load'])
	def postProjectLoad(self, data):
		if 'path' in data.keys():
			path = data['path']
			_typeString = type(path) == str
			if not _typeString:
				self.formatTypeErrorMessage('path', 'str')
				return -1
			else:
				code = 200
				message = 'OK'
				try:
					project.load(path)
				except Exception as e:
					code = 500
					message = 'Internal Server Error'
				finally:
					self.formatResponse(code, message)
		else:
			project.load()
			self.formatResponse(204, 'No Content', {})

	@handleGet(schemas['post_project_save'])
	def postProjectSave(self):
		params = self.parameters
		path = params.get('path') or project.name
		if path.split('.')[-1] != 'toe':
			path += '.toe'
		save = project.save(path)

		if save:
			data = {'success': 'Project saved'}
			self.formatResponse(200, 'OK', data)
		else:
			data = {'error': 'Unknown Error'}
			self.formatResponse(500, 'Internal Server Error', data)

	def postProjectQuit(self):
		self.quit()
		self.formatResponse(200, 'OK', {})
# -------------------------------------------------#
# -------------------- SYSINFO --------------------#
# -------------------------------------------------#

	def getSysInfoNumCpus(self):
		data = {
			'name': 'System CPU Count',
			'scope': 'sysinfo.numCPUs',
			'description': '',
			'built-in': True,
			'data': {
					'value': sysinfo.numCPUs,
					'type': 'int'
			},
			'links': []
		}

		self.formatResponse(200, 'OK', data)

	def getSysInfoRAM(self):
		data = {
			'name': 'System RAM',
			'scope': 'sysinfo.ram',
			'description': '',
			'built-in': True,
			'data': {
					'value': sysinfo.ram,
					'type': 'int'
			}
		}
		self.formatResponse(200, 'OK', data)
# --------------------------------------------#
# -------------------- UI --------------------#
# --------------------------------------------#

	def getUIMasterVolume(self):
		data = {
			'name': 'UI Master Volume',
			'scope': 'ui.masterVolume',
			'description': '',
			'data': {
					'value': ui.masterVolume,
					'type': 'float'
			}
		}
		self.formatResponse(200, 'OK', data)

	@handler(schemas['put_ui_masterVolume'])
	def putUIMasterVolume(self, data):
		volume = data['volume']
		ui.masterVolume = volume
		data = {
			'success': {
				'name': 'UI Master Volume',
				'scope': 'ui.masterVolume',
				'data': {
					'value': ui.masterVolume,
					'type': 'float'
				}
			}
		}
		self.formatResponse(200, 'OK', data)

# ------------------------------------------------------#
# ---------------------- MONITORS ----------------------#
# ------------------------------------------------------#
	def get_monitor(self, index):

		if index == None:
			self.formatResponse(400, 'Bad Format', {})
			return False
		thisMonitor = monitors[index]
		if thisMonitor:
			return thisMonitor
		else:
			self.formatResponse(404, 'Resource Not Found', {})
			return False

	def getMonitors(self):
		monitorsData = []
		monitorLinks = [
			{
				'rel': 'self',
				'href': self.rel_prefix + 'api/banana/monitors'
			}
		]
		for m in range(len(monitors)):
			thisMonitor = {
				'name': monitors[m].displayName,
				'description': monitors[m].description,
				'index': m
			}
			monitorsData.append(thisMonitor)
			link = self.rel_prefix + f'api/banana/monitors/monitor/{m}'
			monitorLinks.append({
				'rel': 'monitors/monitor',
				'href': link
			})
		data = {
			'name': 'Monitors',
			'scope': 'monitors',
			'description': 'Monitors connected to machine',
			'built-in': True,
			'data': {
					'value': monitorsData,
					'type': 'list'
			},
			'links': monitorLinks
		}
		self.formatResponse(200, 'OK', data)

	def getMonitor(self):
		index = int(self.parameters.get('mon'))
		thisMonitor = self.get_monitor(index)
		if thisMonitor:
			data = {
				'name': f'Monitor {index}',
				'scope': 'monitors.monitor',
				'description': 'Description of a monitor instance',
				'built-in': True,
				'data': {
						'description': {
							'value': thisMonitor.description,
							'type': 'str'
						},
					'isPrimary': {
							'value': thisMonitor.isPrimary,
							'type': 'bool'
					},
					'resolution': {
							'width': {
								'value': thisMonitor.width,
								'type': 'int'
							},
							'height': {
								'value': thisMonitor.height,
								'type': 'int'
							}
					},
					'position': {
							'left': {
								'value': thisMonitor.left,
								'type': 'int'
							},
							'right': {
								'value': thisMonitor.right,
								'type': 'int'
							},
							'top': {
								'value': thisMonitor.top,
								'type': 'int'
							},
							'bottom': {
								'value': thisMonitor.bottom,
								'type': 'int'
							}
					},
					'refreshRate': {
							'value': thisMonitor.refreshRate,
							'type': 'float'
					},
					'serialNumber': {
							'value': thisMonitor.serialNumber,
							'type': 'str'
					}
				},
				'links': [{
					'rel': 'self',
					'href': self.rel_prefix + f'api/banana/monitors/monitor/{thisMonitor.index}'
				}]
			}
			self.formatResponse(200, 'OK', data)

		else:
			self.formatResponse(404, 'Resource Not Found', {})

	def getMonitorAttribute(self):
		thisMonitor = self.get_monitor()
		attribute = self.parameters.get('attribute')
		attribute_name = copy.copy(attribute)

		if thisMonitor and attribute:
			attribute = getattr(thisMonitor, attribute)
			data = {
				'name': f'Monitor {attribute_name}',
				'scope': 'monitors.monitor',
				'description': '',
				'built-in': True,
				'data': {
						'value': attribute,
						'type': type(attribute).__name__
				}
			}
			self.formatResponse(200, 'OK', data)
		else:
			self.formatResponse(404, 'Resource Not Found', {})

	def postMonitorsRefresh(self):
		monitors.refresh()
		data = {
			'name': 'Refresh Monitors',
			'scope': 'monitors.refresh',
			'description': '',
			'built-in': True,
			'data': {},
			'links': [
					{
						'rel': 'self',
						'href': self.rel_prefix + 'api/banana/monitors/refresh'
					}
			]
		}
		self.formatResponse(200, 'OK', data)

# -------------------------------------------------------#
# ---------------------- OPERATORS ----------------------#
# -------------------------------------------------------#

	@handleGet(schemas['get_op'])
	def getOp(self):

		path = self.parameters.get('path') or self.parameters.get('id')
		operator = op(path)
		if not operator:
			self.formatResponse(404, 'Resource Not Found', {})
			return
		_id = operator.id
		data = {
			'name': f'Operator {_id}',
			'scope': 'ops',
			'description': '',
			'built-in': True,
			'data': butils.jsonifyOp(operator),
			'links': [
					{
						'rel': 'self',
						'href': self.rel_prefix + f'api/banana/op?id={_id}'
					}
			]
		}
		self.formatResponse(200, 'OK', data)

	@handler(schemas['post_op'])
	def postOp(self, data):
		name = data['name']
		_type = data['type']
		parent = data['parent']

		if not op(parent):
			self.formatResponse(
				409, 'Conflict', {'conflict': 'Parent does not exist.'})
			return

		newOp = op(parent).create(_type, name)
		_id = newOp.id

		data = {
			'name': f'Operator {_id}',
			'scope': 'op',
			'description': '',
			'built-in': True,
			'data': butils.jsonifyOp(newOp),
			'links': [
					{
						'rel': 'self',
						'href': self.rel_prefix + f'api/banana/op?id={_id}'
					}
			]
		}
		self.formatResponse(201, 'Created', data)

	@handler(schemas['delete_op'])
	def deleteOp(self, data):
		path = data.get('path') or data.get('id')
		operator = op(path)
		if not operator:
			data = {
				'error': {
					f'NoneType: operator {path} does not exist.'
				}
			}
			self.formatResponse(404, 'Not Found', data)
		else:
			op(path).destroy()
			self.formatResponse(204, 'No Content', {})

	@handleGet(schemas['get_op_attribute'])
	def getOpAttribute(self):
		path = self.parameters.get('path') or self.parameters.get('id')
		attribute = self.parameters.get('attribute')
		operator = op(path)
		hasAttribute = hasattr(operator, attribute)

		if operator and hasAttribute:
			_id = operator.id
			attributeVal = getattr(operator, attribute)
			data = {
				'name': f'Operator {_id} {attribute}',
				'scope': 'ops.attribute',
				'data': {'value': attributeVal,
						 'type': str(type(attributeVal).__name__)},
				'links': [
						{
							'rel': 'self',
							'href': self.rel_prefix + f'api/banana/op/{attribute}?id={_id}'
						}
				]
			}
			self.formatResponse(200, 'OK', data)
		else:
			data = {'error': 'The operator or attribute does not exist.'}
			self.formatResponse(404, 'Resource Not Found', data)

	@handleGet(schemas['put_op_attribute'])
	def putOpAttribute(self):
		path = self.parameters.get('path') or self.parameters.get('id')
		attribute = self.parameters.get('attribute')
		value = self.parameters.get('val')

		operator = op(path)
		if operator:
			try:
				_type = type(getattr(operator, attribute))
				value = _type(value)
				setattr(operator, attribute, value)
			except Exception as e:
				self.format500(error=type(e).__name__)
				return

			data = {
				'name': 'opserator Attribute',
				'scope': 'ops.attribute',
				'data': {
						'value': value,
						'type': str(type(value).__name__)
				}
			}

			self.formatResponse(200, 'OK', data)
		else:
			self.formatResponse(404, 'Resource Not Found', {})

	def getOpIdMap(self):
		opIdMap = butils.mapOperators()

		data = {
			'name': 'Operator Id Map',
			'scope': 'op.ids',
			'description': 'Dictionary mapping absolute operator paths to their unique ID\'s. Only contains operators that have been explicitly configured.',
			'built-in': False,
			'data': {
					'value': opIdMap,
					'type': 'dict'
			}
		}
		self.formatResponse(200, 'OK', data)

	@handleGet(schemas['get_op_id'])
	def getOpID(self):
		params = self.parameters

		path = params['path']
		operator = op(path)

		if operator:
			_id = operator.id
			data = {
				'name': 'Operator ID',
				'scope': 'op.id',
				'description': 'Unique integer identifier.',
				'built-in': True,
				'data': {
						'value': _id,
						'type': 'int'
				},
				'links': [
					{
						'rel': 'self',
						'href': self.rel_prefix + f'api/banana/op/id?path={path}'
					},
					{
						'rel': 'op',
						'href': self.rel_prefix + f'api/banana/op?id={_id}'
					}
				]
			}
			self.formatResponse(200, 'OK', data)
		else:
			self.formatResponse(404, 'Not Found')

	@handleGet(schemas['get_op_name'])
	def getOpName(self):
		params = self.parameters
		path = params.get('path') or int(params.get('id'))
		operator = op(path)

		if operator:
			name = operator.name
			_id = operator.id
			data = {
				'name': f'Operator {_id} name',
				'scope': 'op.name',
				'description': '',
				'built-in': True,
				'data': {
						'value': name,
						'type': 'str'
				},
				'links': {
					'rel': 'self',
					'href': self.rel_prefix + f'api/banana/op/name?id={_id}'
				}
			}

			self.formatResponse(200, 'OK', data)
		else:
			self.formatResponse(404, 'Resource Not Found', {})

	@handler(schemas['put_op_name'])
	def putOpName(self, data):
		path = data.get('path') or int(data.get('id'))
		name = data.get('name')
		operator = op(path)
		if not operator:
			self.formatResponse(404, 'Resource Not Found', {})
			return -1
		# check for duplicate
		try:
			operator.name = name
		except tdError:
			data = {'conflict': 'Invalid or duplicate operator name.'}
			self.formatResponse(409, 'Conflict', data)
		else:
			data = {
				'success': {
					'name': 'Operator',
					'scope': 'op.name'
				}
			}
			self.formatResponse(200, 'OK', data)

	@handleGet(schemas['get_op_storage'])
	def getOpStorage(self):
		params = self.parameters

		path = params.get('path') or int(params.get('id'))
		operator = op(path)
		if not operator:
			self.formatResponse(404, 'Resource Not Found', {})
			return -1
		if not hasattr(operator, 'storage'):
			self.formatResponse(422, 'Unprocessable Content', {})
			return -1

		data = {
			'name': 'Operator Storage',
			'scope': 'op.storage',
			'description': '',
			'data': {'value': operator.storage,
					 'type': 'dict'}
		}
		try:
			code = 200
			message = 'OK'
			data = json.dumps(data)
		except Exception as e:
			code = 500
			message = 'Internal Server Error'
			data = {'error': str(e)}
		finally:
			self.formatResponse(code, message, data)

	@handleGet(schemas['get_op_tags'])
	def getOpTags(self):
		params = self.parameters

		path = params.get('path') or int(params.get('id'))
		operator = op(path)
		if operator:

			_tags = [tag for tag in operator.tags]
			operatorId = op(path).id
			operatorName = op(path).name
			data = {
				'name': 'Operator Tags',
				'scope': 'op.tags',
				'description': '',
				'data': {'value': _tags,
						 'type': 'set',
						 'items': {'type': 'str'}},
				'operator_name': operatorName,
				'operator_id': operatorId,
				'links': [
						{
							'rel': 'self',
							'href': self.rel_prefix + f'api/banana/op/tags?id={operatorId}'
						}
				]
			}
			self.formatResponse(200, 'OK', data)
		else:
			data = {'error': f'NoneTypeError: op("{path}") does not exist.'}
			self.formatResponse(404, 'Resource Not Found', data)

	@handler(schemas['post_op_tags'])
	def postOpTags(self, data):
		# this might actually be a PATCH
		# There should be a PUT and a PATCH; PUT will replace all tags, PATCH will just add
		path = data.get('path') or int(data.get('id'))
		tags = data['tags']

		operator = op(path)
		if operator:
			for tag in tags:
				operator.tags.add(tag)
			_id = operator.id
			data = {
				'success': {
					'name': f'Operator {_id} tags',
					'scope': 'op.tags',
							'description': '',
							'data': {},
							'links': [
								{
									'rel': 'self',
									'href': self.rel_prefix + f'api/banana/op/tags?id={_id}'
								}
							]
				}
			}
			self.formatResponse(201, 'Created', data)
		else:
			data = {
				'error': f'NoneTypeError: op("{path}") does not exist.'
			}
			self.formatResponse(404, 'Resource Not Found', data)

	@handler(schemas['delete_op_tags'])
	def deleteOpTags(self, data):
		path = data.get('path') or int(data.get('id'))
		tags = data['tags']
		for tag in tags:
			try:
				op(path).tags.remove(tag)
				self.formatResponse(204, 'No Content', {})
			except KeyError:
				self.formatResponse(404, 'Resource Not Found', {})

	@handleGet(schemas['get_op_par'])
	def getOpPar(self):
		params = self.parameters

		path = params.get('path') or int(params.get('id'))
		par = params['par']
		operator = op(path)

		if operator:
			_id = operator.id
			value = operator.par[par].val
			data = {
				'name': f'Operator {_id} parameter {par}',
				'scope': 'ops.par',
				'description': '',
				'data': {
						'value': value,
						'type': type(value).__name__
				}
			}
		self.formatResponse(200, 'OK', data)

	@handleGet(schemas['put_op_par'])
	def putOpPar(self):
		params = self.parameters
		path = params.get('path') or int(params.get('id'))
		par = params['par']
		val = params['val']
		operator = op(path)

		if operator and operator.par[par]:

			operator.par[par].val = val
			data = {
				'success': True
			}
			self.formatResponse(200, 'OK', data)
		else:
			data = {
				'error': 'The operator or parameter does not exist.'
			}
			self.formatResponse(404, 'Resource Not Found', data)
# -------------------------------------------------------------#
# ---------------------- NAMED OPERATORS ----------------------#
# -------------------------------------------------------------#

	def getNamedOps(self):
		pass

	@handleGet(schemas['get_named_op'])
	def getNamedOp(self):
		params = self.parameters
		name = params.get('name')

		operator = op.NAPs.Ops(name)

		data = {
			'success': {
				'data': butils.jsonifyOp(operator)
			}
		}
		self.formatResponse(200, 'OK', data)

	@handleGet(schemas['get_named_op_attribute'])
	def getNamedOpAttribute(self):
		params = self.parameters
		name = params.get('name')
		attribute = params.get('attribute')
		operator = op.NAPs.Ops(name)
		hasAttribute = hasattr(operator, attribute)

		if operator and hasAttribute:
			attributeVal = getattr(operator, attribute)
			data = {
				'name': f'{name} {attribute}',
				'scope': 'namedOps.attributes',
				'description': '',
				'built-in': False,
				'data': {
						'value': attributeVal,
						'type': type(attributeVal).__name__
				}
			}
			self.formatResponse(200, 'OK', data)
		else:
			data = {'error': 'The operator or attribute does not exist.'}
			self.formatResponse(404, 'Resource Not Found', data)

	@handleGet(schemas['put_named_op_attribute'])
	def putNamedOpAttribute(self):
		params = self.parameters
		name = params.get('name')
		attribute = params.get('attribute')
		value = params.get('value')
		operator = op.NAPs.Ops(name)
		_type = type(getattr(operator, attribute))

		try:
			if _type == bool:
				value = butils.stringToBool(value)
			else:
				value = _type(value)

			setattr(operator, attribute, value)
			data = {
				'success': {
					'name': f'Operator {name} {attribute}',
					'scope': 'namedOps.attributes',
					'description': '',
					'data': {'value': value,
							 'type': 'bool'}
				}
			}
			self.formatResponse(200, 'OK', data)
		except ValueError as ve:
			data = {
				'error': {'message': 'ValueError: Value could not be coerced to the Attribute\'s type'}
			}
			self.formatResponse(400, 'Bad Request', data)
		except AttributeError as ae:
			data = {
				'error': {'message': 'AttributeError: It is likely that the attribute is not writable.'}
			}
			self.formatResponse(400, 'Bad Request', data)
		except Exception as e:
			data = {'error': {'message': 'UnknownError'}}
			self.formatResponse(500, 'Internal Server Error', data)

	@handleGet(schemas['get_named_op_par'])
	def getNamedOpPar(self):
		params = self.parameters
		name = params.get('name')
		par = params.get('par')

		operator = op.NAPs.Ops(name)
		parVal = operator.par[par].val

		data = {
			'name': 'Operator Parameter',
			'scope': 'NAPs.Ops.par',
			'description': '',
			'built-in': False,
			'data': {'value': parVal,
					 'type': type(parVal).__name__}
		}
		self.formatResponse(200, 'OK', data)

	@handleGet(schemas['put_named_op_par'])
	def putNamedOpPar(self):
		params = self.parameters
		name = params.get('name')
		par = params.get('par')
		value = params.get('val')
		operator = op.NAPs.Ops(name)
		if operator:
			opPar = operator.par[par]
			if opPar:
				try:
					opPar.val = value
				except:
					pass
			data = {'success': {}}
			self.formatResponse(200, 'OK', data)
		else:
			self.formatResponse(404, 'Resource Not Found', {})
# --------------------------------------------------------------#
# ---------------------- NAMED PARAMETERS ----------------------#
# --------------------------------------------------------------#

	def getNamedPars(self):
		pass

	@handleGet(schemas['get_named_par'])
	def getNamedPar(self):
		params = self.parameters
		name = params.get('name')
		par = op.NAPs.Pars(name)
		if par:
			value = par.val
			data = {
				'name': name,
				'scope': 'namedPars',
				'description': '',
				'data': {'value': value,
						 'type': type(value).__name__}
			}
			self.formatResponse(200, 'OK', data)
		else:
			data = {
				'error': f'{name} is not a Named Parameter.'
			}
			self.formatResponse(404, 'Resource Not Found', data)

	@handler(schemas['put_named_par'])
	def putNamedPar(self, data):

		parameter = data.get('parameter')
		_type = parameter.get("type")
		if _type == "scalar":
			name = parameter.get('name')
			value = parameter.get('value')
			if not (name and value):
				data = {
					'error':'Missing `name` or `value`.'
				}
				self.formatResponse(400, 'Bad Format', data)
				return
			par = op.NAPs.Pars(name)
			if par:
				_type = type(getattr(par, 'val'))
				try:
					value = _type(value)
				except:
					data = {
						'error': 'Value could not be coerced to the appropriate type'}
					self.formatResponse(422, 'Unprocessable Content', data)
				else:
					par.val = value
					data = {'success': {}}
					self.formatResponse(200, 'OK', data)

		elif _type == "vector":
			name = parameter.get('name')
			value = parameter.get('value')

			if not value:
				data = {
					'error':'At least one scalar parameter is missing a value.'
				}
				self.formatResponse(400, 'Bad Format', data)
				return
			par = op.NAPs.Pars(name)
			if par:
				data = {'success':[] }
				for param in value:
					_name = param.get('name')  # name of scalar
					_value = param.get('value')  # value of scalar
					_par = par[_name]			# scalar par object

					if not _par:
						data = {
						'error':f'{_name} is not a parameter.'
						}
						self.formatResponse(404, 'Resource Not Found', data)
					_type = type(getattr(_par, 'val'))
					print(_type)
					try:
						_value = _type(_value)
					except:
						data = {'error': 'Value could not be coerced to the appropriate type'}
						self.formatResponse(422, 'Unprocessable Content', data)
						return
					else:
						_par.val = _value
						_data = {_name: {
								'value': _par.val,
								'type': _type.__name__
								}}
						data.append(_data)
				
				self.formatResponse(200, 'OK', data)
			else:
				data = {
					'error':f'{name} is not a Named Parameter.'
				}
				self.formatResponse(404, 'Resource Not Found', data)

		else:
			data = {'error': 'No acceptable type found.'}
			self.formatResponse(422, 'Unprocessable Content', data)

