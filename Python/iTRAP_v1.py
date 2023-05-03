import json
from functools import wraps
schemas = mod('schemas').schemas
ttree = mod('ttree_builder')
permissions = mod('Permissions')
permissions_config_dat = op('permissions_config')
permissions_config = json.loads(permissions_config_dat.text)




class ITRAP():
	routing_table = {}
	routing_tree = ttree.Trie()

	def __init__(self, thisComp):
		self.thisComp = thisComp
		self.itrap_port = thisComp.par.Port
		self.ip_address = thisComp.par.Ipaddress

		if not me.parent().storage.get('Permissions'):
			me.parent().store('Permissions',{})
		print(thisComp)

		self.routing_table = {
			"/api/banana/app/architecture": {'handlers': {'GET': self.getAppArchitecture}, 'scope': 'app.architecture'},
			"/api/banana/app/build": {'handlers':{'GET': self.getAppBuild}, 'scope':'app.build'},
			"/api/banana/app/launchTime": {'handlers':{'GET': self.getAppLaunchTime}, 'scope':'app.launchTime'},
			"/api/banana/app/startTimestamp": {'handlers':{'GET': self.getAppStartTimestamp}, 'scope':'app.startTimestamp'},
			"/api/banana/app/osName": {'handlers':{'GET': self.getAppOSName}, 'scope':'app.osName'},
			"/api/banana/app/power": {'handlers':{'GET': self.getAppPower, 'PUT': self.putAppPower}, 'scope':'app.power'},
			"/api/banana/app/product": {'handlers':{'GET': self.getAppProduct}, 'scope':'app.product'},
			"/api/banana/app/version": {'handlers':{'GET': self.getAppVersion}, 'scope':'app.version'},
			"/api/banana/app/play": {'handlers':{'GET': self.getAppPlay, 'PUT': self.putAppPlay}, 'scope':'app.play'},
			"/api/banana/project/name": {'handlers':{'GET': self.getProjectName}, 'scope':'project.name'},
			"/api/banana/project/saveVersion": {'handlers':{'GET': self.getProjectSaveVersion}, 'scope':'project.saveVersion'},
			"/api/banana/project/saveBuild": {'handlers':{'GET': self.getProjectSaveBuild}, 'scope':'project.saveBuild'},
			"/api/banana/project/saveTime": {'handlers':{'GET': self.getProjectSaveTime}, 'scope':'project.saveTime'},
			"/api/banana/project/saveOSName": {'handlers':{'GET': self.getProjectSaveOSName}, 'scope':'project.saveOSName'},
			"/api/banana/project/saveOSVersion": {'handlers':{'GET': self.getProjectSaveOSVersion}, 'scope':'project.saveOSVersion'},
			"/api/banana/project/paths": {'handlers':{'GET': self.getProjectPaths}, 'scope':'project.paths'},
			"/api/banana/project/cookRate": {'handlers':{'GET': self.getProjectCookRate, 'PUT': self.putProjectCookRate}, 'scope':'project.cookRate'},
			"/api/banana/project/realTime": {'handlers':{'GET': self.getProjectRealTime, 'PUT': self.putProjectRealTime}, 'scope':'project.'},
			"/api/banana/project/performOnStart": {'handlers':{'GET': self.getProjectPerformOnStart, 'PUT': self.putProjectPerformOnStart}, 'scope':'project.performOnStart'},
			"/api/banana/project/load": {'handlers':{'POST': self.postProjectLoad}, 'scope':'project.load'},
			"/api/banana/project/save": {'handlers':{'POST': self.postProjectSave}, 'scope':'project.save'},
			"/api/banana/project/quit": {'handlers':{'POST': self.postProjectQuit}, 'scope':'project.quit'},
			"/api/banana/sysinfo/numCPUs": {'handlers':{'GET': self.getSysInfoNumCpus}, 'scope':'sysinfo.numCPUs'},
			"/api/banana/sysinfo/ram": {'handlers':{'GET': self.getSysInfoRAM}, 'scope':'sysinfo.ram'},
			"/api/banana/ui/masterVolume": {'handlers':{'GET': self.getUIMasterVolume, 'PUT': self.putUIMasterVolume}, 'scope':'ui.masterVolume'},
			"/api/banana/monitors": {'handlers':{'GET': self.getMonitors}, 'scope':'monitors.'},
			"/api/banana/monitors/refresh": {'handlers':{'POST': self.postMonitorsRefresh}, 'scope':'monitors.refresh'},
			"/api/banana/op": {'handlers':{'GET': self.getOp, 'POST': self.postOp, 'DELETE': self.deleteOp}, 'scope':'op'},
			"/api/banana/op/opIdMap": {'handlers':{'GET': self.getOpIdMap}, 'scope':'op.opIdMap'},
			"/api/banana/op/id": {'handlers':{'GET': self.getOpID}, 'scope':'op.id'},
			"/api/banana/op/id/<op-id>/par/<par-name>": {'handlers':{'GET': self.getOpPar}, 'scope':'op.par'},
			"/api/banana/op/id/<id>/par/<par>/val/<val>": {'handlers':{'PUT': self.putOpPar}, 'scope':'op.par.val'},
			"/api/banana/op/name": {'handlers':{'GET': self.getOpName, 'PUT': self.putOpName}, 'scope':'op.name'},
			"/api/banana/op/storage": {'handlers':{'GET': self.getOpStorage}, 'scope':'op.storage'},
			"/api/banana/op/tags": {'handlers':{'GET': self.getOpTags, 'POST': self.postOpTags, 'DELETE': self.deleteOpTags}, 'scope':'op.tags'},
			"/api/banana/op/par": {'handlers':{'GET': self.getOpPar, 'PUT': self.putOpPar}, 'scope':'op.par'},
			"/api/banana/namedOp/<name>": {'handlers':{'GET': self.getNamedOp}, 'scope':'namedOp'},
			"/api/banana/namedOp/<name>/attribute/<attribute>": {'handlers':{'GET': self.getNamedOpAttribute, 'PUT': self.putNamedOpAttribute}, 'scope':'namedOp.attribute'},
			"/api/banana/namedOp/<name>/par/<par>": {'handlers':{'GET': self.getNamedOpPar}, 'scope':'namedOp.par'}
		}

		for key, val in self.routing_table.items():
			handlers = val.get('handlers')
			scope = val.get('scope')
			self.routing_tree.insert(key, handlers, scope)
		

	def CreateKey(self, user):
		permission = permissions.Permission(user, permissions_config)
		key = permission.key
		permissions_config[user].update({'key':permission.key})
		permissions_config_dat.text = json.dumps(permissions_config)
		me.parent().storage["Permissions"].update({key:permission})

	def handler(thisSchema):
		def decorator(func):
			@wraps(func)
			def wrapper(self, *args, **kwargs):
				data = json.loads(self.request['data'])
				params = data.get('params')
				schema = thisSchema
				if not params:
					params = self.parameters
				hasParams, validTypes = self.validateParameters(data, schema)
				if hasParams and validTypes:
					# this will require some rework, but can pass deserialized data through params
					func(self, *args, **kwargs)
				else:
					self.formatResponse(400, 'Bad Request', {})
			return wrapper
		return decorator

	def handleGet(thisSchema):
		def decorator(func):
			@wraps(func)
			def wrapper(self, *args, **kwargs):
				params = self.parameters
				schema = thisSchema

				hasParams, validTypes = self.validateParameters(params, schema)

				if hasParams and validTypes:
					func(self, *args, **kwargs)
				else:
					self.formatResponse(400, 'Bad Request', {})
			return wrapper
		return decorator

	def mapOperators(self):
		'''
						Gets id of each path listed in the specified table
						Then builds a dictionary of form:
						<operator-name>:{
										'path':<op-path>,
										'id':<op-id>
						}
		'''
		operator_id_map = {}
		for row in op("map_operator_ids/operator_id_map").rows():
			path = row[0].val
			operator = op(path)

			_id = operator.id
			name = operator.name
			row[1].val = _id

			_map = {
				'path': path,
				'id': _id
			}
			operator_id_map[name] = _map

		return operator_id_map

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

	def validateParameters(self, pars: dict, schema):
		included_pars = pars.keys()
		expected_pars = schema['parameters']
		required_pars = schema['required']

		hasRequired = True
		validType = False
		for p in required_pars:
			'''
			GPT: suggests using isinstance() instead of type()
			Second arg of isinstance can be a tuple of acceptable types
			'''
			if type(p) == str:
				# `p in included_pars` will return boolean True or False
				# if not included, hasRequired permanently False
				hasRequired = hasRequired and (p in included_pars)
			if type(p) == tuple:
				hasTupleOption = False
				for _p in p:
					hasTupleOption = hasTupleOption or (_p in included_pars)
				hasRequired = hasRequired and hasTupleOption
				# check if one of these is present
				pass
		if hasRequired:
			validType = True
			for par, val in pars.items():

				expected_type = expected_pars[par]['type']
				if type(expected_type) == tuple:

					validType = False
					for _type in expected_type:

						validType = validType or (_type == type(val))
						#
						if not validType:
							try:
								_type(val)
								validType = validType or True
							except:
								pass
						#
				else:
					validType = validType and (expected_type == type(val))
					#
					if not validType:
						try:
							expected_type(val)
							validType = validType or True
						except:
							pass
					#
		print(hasRequired, validType)
		return hasRequired, validType

# --------------------------------------------------------#
# -------------------- BEGIN HANDLERS --------------------#
# --------------------------------------------------------#

#---------------------- APPLICATION ----------------------#

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
			'data': {
					'value': app.launchTime,
					'type': 'float'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/app/launchTime'
				},{
					'rel':'app.startTimestamp',
					'href': self.rel_prefix + 'api/banana/app/startTimestamp'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppStartTimestamp(self):
		timestamp = op('records')['startTimestamp', 'value'].val
		data = {
			'name': 'Application Start Time',
			'scope': 'app.startTimestamp',
			'description': 'UNIX timestamp recorded when the application launches.',
			'built-in': False,
			'data': {
					'value': timestamp,
					'type': 'float'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/app/startTimestamp'
				},{
					'rel':'app.launchTime',
					'href':self.rel_prefix + 'api/banana/app/launchTime'
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
			'id': 'app.power',
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
	def putAppPower(self):
		data = json.loads(self.request['data'])

		power = data["state"]
		app.power = power

		data = {
			'success': {
				'name': 'Application Power',
				'id': 'app.power',
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
				},{
					'rel': 'app.version',
					'href': self.rel_prefix + 'api/banana/app/version'
				},
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppVersion(self):
		data = {
			'name': 'Application Version',
			'id': 'app.version',
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
				},{
					'rel':'app.product',
					'href':self.rel_prefix + 'api/banana/app/product'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppPlay(self):
		data = {
			'name': 'Application Transport State',
			'id': 'custom.app.play',
			'description': 'Indicates whether the application is playing or stopped.',
			'built-in': False,
			'data': {
					'value': op('/local/time').play,
					'type': 'bool'
			}
		}

		self.formatResponse(200, 'OK', data)

	@handler(schemas['put_app_play'])
	def putAppPlay(self):
		data = json.loads(self.request['data'])

		play = data['play']

		op("/local/time").play = play
		data = {
			'sucess': {
				'name': 'Application Transport State',
				'id': 'custom.app.play',
				'data': {
						'value': op("/local/time").play,
						'type': {
							"oneOf": [
								'boolean',
								'integer'
							]
						}
				}
			}
		}
		self.formatResponse(200, 'OK', data)

#---------------------- PROJECT ----------------------#
	def getProjectName(self):
		data = {
			'name': 'Project Name',
			'scope': 'project.name',
			'description': 'The filename under which the project is saved.',
			'built-in': True,
			'data': {
					'value': project.name,
					'type': 'str'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/banana/project/name'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getProjectPaths(self):
		data = {
			'name': 'Project Paths',
			'scope': 'project.paths',
			'description': 'A dictionary which can be used to define URL-syntax path prefixes, enabling you to move your media to different locations easily.',
			'built-in': True,
			'data': {
					'value': project.paths,
					'type': 'dict'
			}
		}
		self.formatResponse(200, "OK", data)

	def postProjectPaths(self):
		pass

	def putProjectPaths(self):
		pass

	def getProjectCookRate(self):
		data = {
			'name': 'Project Cook Rate',
			'scope': 'project.cookRate',
			'description': 'The maximum number of frames processed each second.',
			'built-in': True,
			'data': {
					'value': project.cookRate,
					'type': 'float'
			}
		}
		self.formatResponse(200, "OK", data)

	@handler(schemas['put_project_cookRate'])
	def putProjectCookRate(self):
		data = json.loads(self.request['data'])

		rate = data['rate']
		project.cookRate = rate
		data = {
			'name': 'Project Cook Rate',
			'scope': 'project.cookRate',
			'data': {
					'value': project.cookRate,
					'type': 'float'
			}

		}
		self.formatResponse(200, 'OK', data)
		# else:
		# 	self.formatResponse(400, 'Bad Format', {})

	def getProjectSaveVersion(self):
		data = {
			'name': 'Project Save Version',
			'scope': 'project.saveVersion',
			'description': 'The App version number when the project was last saved.',
			'built-in': True,
			'data': {
					'value': project.saveVersion,
					'type': 'str'
			}
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
			}
		}

		self.formatResponse(200, 'OK', data)

	def getProjectSaveTime(self):
		return

	def getProjectSaveOSName(self):
		return

	def getProjectSaveOSVersion(self):
		return

	def getProjectRealTime(self):
		data = {
			'name': 'Project Real Time',
			'scope': 'project.realTime',
			'description': 'Realtime cooking state. When True, frames may be skipped in order to maintain the cookRate.',
			'built-in': True,
			'data': {
					'value': project.realTime,
					'type': 'bool'
			}
		}
		self.formatResponse(200, 'OK', data)

	@handler(schemas['put_project_realTime'])
	def putProjectRealTime(self):
		data = json.loads(self.request['data'])
		realTime = data['realTime']

		project.realTime = realTime
		data = {
			'name': 'Project Real Time',
			'scope': 'project.realTime',
			'data': {
					'value': project.realTime,
					'type': 'bool'
			}
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
			}
		}
		self.formatResponse(200, 'OK', data)

	@handler(schemas['put_project_performOnStart'])
	def putProjectPerformOnStart(self):
		data = json.loads(self.request['data'])

		performOnStart = data['performOnStart']

		project.performOnStart = performOnStart
		data = {
			'name': 'Project Perform on Start',
			'scope': 'project.performOnStart',
			'data': {
					'value': project.performOnStart,
					'type': 'bool'
			}
		}
		self.formatResponse(200, 'OK', data)

	@handler(schemas['post_project_load'])
	def postProjectLoad(self):
		data = json.loads(self.request['data'])
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
			self.formatResponse(204, 'No Content')

	@handler(schemas['post_project_save'])
	def postProjectSave(self):
		data = json.loads(self.request['data'])
		if 'path' in data.keys():
			path = data['path']
			project.save(path)  # what if this returns an error?
		else:
			project.save()

		self.formatResponse(204, 'No Content', {})

	def postProjectQuit(self):
		self.quit()
		data = {}
		self.formatResponse(204, 'No Content', data)

	def getSysInfoNumCpus(self):
		data = {
			'name': 'Sysinfo CPU Count',
			'scope': 'sysinfo.numCPUs',
			'description': '',
			'data': {
					'value': sysinfo.numCPUs,
					'type': int
			}
		}

		self.formatResponse(200, 'OK', data)

	def getSysInfoRAM(self):
		data = {
			'name': 'Sysinfo RAM',
			'scope': 'sysinfo.ram',
			'description': '',
			'data': {
					'value': sysinfo.ram,
					'type': int
			}
		}
		self.formatResponse(200, 'OK', data)

	def getSysInfoRes(self):
		return

	def getSysInfoNumMonitors(self):
		return

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
	def putUIMasterVolume(self):
		data = json.loads(self.request['data'])

		volume = data['volume']
		ui.masterVolume = volume
		data = {
			'name': 'UI Master Volume',
			'id': 'ui.masterVolume',
			'data': {
					'value': ui.masterVolume,
					'type': 'float'
			}
		}
		self.formatResponse(200, 'OK', data)

	def getMonitors(self):
		monitorsData = []
		monitorLinks = [{
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
			link = self.rel_prefix + f'api/banana/monitors/{m}'
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

	def postMonitorsRefresh(self):
		return
############# OPERATORS ############

	@handleGet(schemas['get_op'])
	def getOp(self):

		path = self.parameters.get('path') or self.parameters.get('id')
		operator = op(path)

		data = {
			'success': 'I will format later'
		}
		self.formatResponse(200, 'OK', data)

	@handler(schemas['post_op'])
	def postOp(self):
		data = json.loads(self.request['data'])

		name = data['name']
		_type = data['type']
		parent = data['parent']
		newOp = op(parent).create(_type, name)

		# need to check if parent exists
		data = {
			'name-space': 'Operator',
			'id-space': 'op',
			'data': {
				'name': newOp.name,
				'id': newOp.id,
				'path': newOp.path,
				'type': {
						'family': newOp.family,
						'label': newOp.label,
						'type': newOp.type,
						'subType': newOp.subType,
						'OPType': newOp.OPType

				},
				'time': newOp.time.path,
				'flags': [
					'activeViewer',
					'allowCooking',
					'bypass',
					'cloneImmune',
					'current',
					'display',
					'comment'
				]
			}
		}
		self.formatResponse(201, 'Created', data)

	@handler(schemas['delete_op'])
	def deleteOp(self):
		data = json.loads(self.request['data'])
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
			self.formatResponse(204, 'No Content')

	def getOpIdMap(self):
		opIdMap = self.mapOperators()

		data = {
			'name': 'Operator Id Map',
			'id': 'op("mapped_operator_ids")',
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
				'id': 'op.id',
				'description': 'Unique integer identifier.',
				'built-in': True,
				'data': {
						'value': _id,
						'type': 'int'
				}
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
			data = {
				'name': 'Operator Name',
				'scope': 'op.name',
				'description': '',
				'built-in': True,
				'data': {
						'value': name,
						'type': 'str'
				}
			}

			self.formatResponse(200, 'OK', data)
		else:
			self.formatResponse(404, 'Resource Not Found', {})

	@handler(schemas['put_op_name'])
	def putOpName(self):
		data = json.loads(self.request['data'])

		path = data.get('path') or int(data.get('id'))
		name = data.get('name')
		operator = op(path)
		if not operator:
			self.formatResponse(404, 'Resource Not Found', {})
			return -1
		operator.name = name

		data = {
			'success': {
				'name': 'Operator',
				'id': 'op.name'
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
			'id': 'op.storage',
			'description': '',
			'data': {
					'value': operator.storage,
					'type': 'dict'
			}
		}
		try:
			code = 200
			message = 'OK'
			json.dumps(data)
		except Exception as e:
			code = 500
			message = 'Internal Server Error'
			data = {
				'error': {
					'message': f'EXCEPTION: {str(e)}'
				}
			}
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
				'data': {
						'value': _tags,
						'type': 'set',
						'items': {
							'type': 'str'
						}
				},
				'operator_name': operatorName,
				'operator_id': operatorId
			}
			self.formatResponse(200, 'OK', data)
		else:
			data = {
				'error': f'NoneTypeError: op("{path}") does not exist.'
			}
			self.formatResponse(404, 'Resource Not Found', data)

	@handler(schemas['post_op_tags'])
	def postOpTags(self):
		# this might actually be a PATCH
		# There should be a PUT and a PATCH; PUT will replace all tags, PATCH will just add
		data = json.loads(self.request['data'])

		path = data.get('path') or int(data.get('id'))
		tags = data['tags']

		operator = op(path)
		if operator:
			for tag in tags:
				operator.tags.add(tag)
			data = {'message': 'Format this!!'}
			self.formatResponse(201, 'Created', data)
		else:
			data = {
				'error': f'NoneTypeError: op("{path}") does not exist.'
			}
			self.formatResponse(404, 'Resource Not Found', data)

	@handler(schemas['delete_op_tags'])
	def deleteOpTags(self):
		data = json.loads(self.request['data'])
		path = data.get('path') or int(data.get('id'))
		tags = data['tags']
		for tag in tags:
			try:
				op(path).tags.remove(tag)
				self.formatResponse(200, 'OK', {})
			except KeyError:
				self.formatResponse(404, 'Resource Not Found', {})

	@handleGet(schemas['get_op_par'])
	def getOpPar(self):
		params = self.parameters

		path = params.get('path') or int(params.get('id'))
		par = params['name']
		operator = op(path)
		if operator:
			value = operator.par[par].val
		# value = op(path).par[param].val
			data = {
				'data': value
			}
		self.formatResponse(200, 'OK', data)

	@handleGet(schemas['put_op_par'])
	def putOpPar(self):
		params = self.parameters
		path = params.get('path') or int(params.get('id'))
		par = params['par']
		val = params['val']
		operator = op(path)
		if operator:

			operator.par[par].val = val
			data = {
				'success': True
			}
		self.formatResponse(200, 'OK', data)

	@handleGet(schemas['get_named_op'])
	def getNamedOp(self):
		params = self.parameters
		name = params.get('name')

		operator = op.NAPs.Ops(name)

		data = {
			'success': True
		}
		self.formatResponse(200, 'OK', data)

	@handleGet(schemas['get_named_op_attribute'])
	def getNamedOpAttribute(self):
		params = self.parameters
		name = params.get('name')
		attribute = params.get('attribute')

		operator = op.NAPs.Ops(name)
		attributeVal = getattr(operator, attribute)

		data = {
			'name': 'Operator Attribute',
			'scope': 'op.attribs',
			'description': '',
			'built-in': False,
			'data': {
					'value': attributeVal,
					'type': type(attributeVal).__name__
			}
		}

		self.formatResponse(200, 'OK', data)

	@handleGet(schemas['put_named_op_attribute'])
	def putNamedOpAttribute(self):
		params = self.parameters
		name = params.get('name')
		attribute = params.get('attribute')
		value = params.get('value')

		operator = op.NAPs.Ops(name)
		_type = type(getattr(operator, attribute))
		try:
			value = _type(value)
			setattr(operator, attribute, value)
			data = {
				'name': 'Operator Attribute',
				'scope': 'NAPs.Ops.attr',
				'description': '',
				'data': {
						'success': True
				}
			}
			self.formatResponse(200, 'OK', data)
		except Exception as e:
			if e == ValueError:
				data = {
					'error': {
						'message': 'ValueError: Value could not be coerced to the Attribute\'s type'
					}
				}
			elif e == AttributeError:
				data = {
					'error': {
						'message': 'AttributeError: It is likely that the attribute is not writable.'
					}
				}
			else:
				data = {
					'error': {
						'message': 'UnknownError'
					}
				}
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
			'data': {
					'value': parVal,
					'type': type(parVal).__name__
			}
		}
		self.formatResponse(200, 'OK', data)
	'''
	def HandleRequest(self, request, response):
		self.request = request
		self.response = response
		self.parameters = request['pars']
		method = request['method']
		uri = request['uri']


		self.response['content-type'] = 'application/json'
		# self.ip_address = socket.gethostbyname(socket.gethostname())
		self.rel_prefix = f'http://{self.ip_address}:{self.itrap_port}/'
		route = f'{method} {uri}'
		try:
			self.routing_table[route]()
		except:
			print('exception')
			func = self.routing_table[route][0]
			args = self.routing_table[route][1]
			func(args)

		# formatResponse(self.response, 200, 'OK', data)

		return self.response
	'''

	def HandleRequest(self, request, response):
		self.request = request
		self.response = response
		self.parameters = request['pars']

		uri = request['uri']
		method = request['method']

		self.response['content-type'] = 'application/json'
		# self.ip_address = socket.gethostbyname(socket.gethostname())
		self.rel_prefix = f'http://{self.ip_address}:{self.itrap_port}/'

		handler, params, scope = self.routing_tree.find(uri, method)

		if params:
			# self.parameters = params
			self.parameters.update(params)

		print('uri')
		if uri.split('/')[2] == 'monkey':
			print('monkey')
			handler(self)
		else:
			handler()

		return self.response

	def format500(self, data=None, error='unknown'):
		if not data:
			data = {
				'error': {
					'message': f'Server encountered an exception while encoding return data.',
					'exception': error
				}
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

	def formatSuccess(self, data):

		self.response['statusCode'] = 200
		self.response['statusReason'] = 'OK'
		responseData = {
			'success': True,
			'data': data
		}
		data = json.dumps(responseData)

		self.response['data'] = data

	def InsertRoute(self, url: str, handlers: dict):
		self.url = url
		url = '/api/monkey' + url
		self.routing_tree.insert(url, handlers)
