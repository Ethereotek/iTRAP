import json
import socket
from functools import wraps
schemas = mod('schemas').schemas
ttree = mod('ttree_builder')


def TestHandler(func):
	def wrapper(*args, **kwargs):
		request = kwargs['request'],
		parameters = kwargs['parameters']
		data = json.loads(request['data'])
		params = data.get('params')
		schema = kwargs.get('schema')
		if not params:
			params = parameters

		schema = schemas[schema]
		hasParams, validTypes = validateParameters(data, schema)

		if hasParams and validTypes:
			func(*args, **kwargs)
		else:
			formatResponse(400, 'Bad Request', {})
	return wrapper


class ITRAP():
	routing_table = {}
	routing_tree = ttree.Trie()
	def __init__(self, thisComp):
		self.thisComp = thisComp
		self.itrap_port = thisComp.par.Port
		self.ip_address = thisComp.par.Ipaddress
		print(thisComp)
		# self.routing_table = {
		# 	"GET /api/v1/app/architecture": self.getAppArchitecture,
		# 	"GET /api/v1/app/build": self.getAppBuild,
		# 	"GET /api/v1/app/launchTime": self.getAppLaunchTime,
		# 	"GET /api/v1/app/startTimestamp":self.getAppStartTimestamp,
		# 	"GET /api/v1/app/osName": self.getAppOSName,
		# 	"GET /api/v1/app/power": self.getAppPower,
		# 	"PUT /api/v1/app/power": [self.putAppPowerN, schemas['put_app_power']],
		# 	"GET /api/v1/app/product": self.getAppProduct,
		# 	"GET /api/v1/app/version": self.getAppVersion,
		# 	"GET /api/v1/app/play": self.getAppPlay,
		# 	"PUT /api/v1/app/play": self.putAppPlay,
		# 	"GET /api/v1/project/name": self.getProjectName,
		# 	"GET /api/v1/project/saveVersion": self.getProjectSaveVersion,
		# 	"GET /api/v1/project/saveBuild": self.getProjectSaveBuild,
		# 	"GET /api/v1/project/saveTime": self.getProjectSaveTime,
		# 	"GET /api/v1/project/saveOSName": self.getProjectSaveOSName,
		# 	"GET /api/v1/project/saveOSVersion": self.getProjectSaveOSVersion,
		# 	"GET /api/v1/project/paths": self.getProjectPaths,
		# 	"GET /api/v1/project/cookRate": self.getProjectCookRate,
		# 	"PUT /api/v1/project/cookRate": self.putProjectCookRate,
		# 	"GET /api/v1/project/realTime": self.getProjectRealTime,
		# 	"PUT /api/v1/project/realTime": self.putProjectRealTime,
		# 	"GET /api/v1/project/performOnStart": self.getProjectPerformOnStart,
		# 	"PUT /api/v1/project/performOnStart": self.putProjectPerformOnStart,
		# 	"POST /api/v1/project/load": self.postProjectLoad,
		# 	"POST /api/v1/project/save": self.postProjectSave,
		# 	"POST /api/v1/project/quit": self.postProjectQuit,
		# 	"GET /api/v1/sysinfo/numCPUs": self.getSysInfoNumCpus,
		# 	"GET /api/v1/sysinfo/ram": self.getSysInfoRAM,
		# 	"GET /api/v1/ui/masterVolume": self.getUIMasterVolume,
		# 	"PUT /api/v1/ui/masterVolume": self.putUIMasterVolume,
		# 	"GET /api/v1/monitors": self.getMonitors,
		# 	"POST /api/v1/monitors/refresh": self.postMonitorsRefresh,
		# 	"GET /api/v1/op": self.getOp,
		# 	"POST /api/v1/op": self.postOp,
		# 	"DELETE /api/v1/op": self.deleteOp,
		# 	"GET /api/v1/op/opIdMap": self.getOpIdMap,
		# 	"GET /api/v1/op/id": self.getOpID,
		# 	"GET /api/v1/op/name": self.getOpName,
		# 	"PUT /api/v1/op/name": self.putOpName,
		# 	"GET /api/v1/op/storage": self.getOpStorage,
		# 	"GET /api/v1/op/tags": self.getOpTags,
		# 	"POST /api/v1/op/tags": self.postOpTags,
		# 	"DELETE /api/v1/op/tags": self.deleteOpTags,
		# 	"GET /api/v1/op/par": self.getOpPar,
		# 	"PUT /api/v1/op/par": self.putOpPar,
		# }
		self.routing_table = {
			"/api/v1/app/architecture": {'GET': self.getAppArchitecture},
			"/api/v1/app/build": {'GET': self.getAppBuild},
			"/api/v1/app/launchTime": {'GET': self.getAppLaunchTime},
			"/api/v1/app/startTimestamp": {'GET': self.getAppStartTimestamp},
			"/api/v1/app/osName": {'GET': self.getAppOSName},
			"/api/v1/app/power": {
				'GET': self.getAppPower,
				'PUT': self.putAppPower
			},

			"/api/v1/app/product": {'GET': self.getAppProduct},
			"/api/v1/app/version": {'GET': self.getAppVersion},
			"/api/v1/app/play": {'GET': self.getAppPlay,
								 'PUT': self.putAppPlay},

			"/api/v1/project/name": {'GET': self.getProjectName},
			"/api/v1/project/saveVersion": {'GET': self.getProjectSaveVersion},
			"/api/v1/project/saveBuild": {'GET': self.getProjectSaveBuild},
			"/api/v1/project/saveTime": {'GET': self.getProjectSaveTime},
			"/api/v1/project/saveOSName": {'GET': self.getProjectSaveOSName},
			"/api/v1/project/saveOSVersion": {'GET': self.getProjectSaveOSVersion},
			"/api/v1/project/paths": {'GET': self.getProjectPaths},
			"/api/v1/project/cookRate": {'GET': self.getProjectCookRate,
										 'PUT': self.putProjectCookRate},

			"/api/v1/project/realTime": {'GET': self.getProjectRealTime,
										 'PUT': self.putProjectRealTime},

			"/api/v1/project/performOnStart": {'GET': self.getProjectPerformOnStart, 'PUT': self.putProjectPerformOnStart},
			"/api/v1/project/load": {'POST': self.postProjectLoad},
			"/api/v1/project/save": {'POST': self.postProjectSave},
			"/api/v1/project/quit": {'POST': self.postProjectQuit},
			"/api/v1/sysinfo/numCPUs": {'GET': self.getSysInfoNumCpus},
			"/api/v1/sysinfo/ram": {'GET': self.getSysInfoRAM},
			"/api/v1/ui/masterVolume": {'GET': self.getUIMasterVolume,
										'PUT': self.putUIMasterVolume},

			"/api/v1/monitors": {'GET': self.getMonitors},
			"/api/v1/monitors/refresh": {'POST': self.postMonitorsRefresh},
			"/api/v1/op": {'GET': self.getOp, 'POST': self.postOp, 'DELETE': self.deleteOp},
			"/api/v1/op/opIdMap": {'GET': self.getOpIdMap},
			"/api/v1/op/id": {'GET': self.getOpID},
			"/api/v1/op/id/<op-id>/par/<par-name>": {'GET':self.getOpPar},
			"/api/v1/op/id/<id>/par/<par>/val/<val>":{'PUT':self.putOpPar},
			"/api/v1/op/name": {'GET': self.getOpName, 'PUT': self.putOpName},
			"/api/v1/op/storage": {'GET': self.getOpStorage},
			"/api/v1/op/tags": {'GET': self.getOpTags, 'POST': self.postOpTags, 'DELETE': self.deleteOpTags},
			"/api/v1/op/par": {'GET': self.getOpPar, 'PUT': self.putOpPar},
		}

		for key, val in self.routing_table.items():
			self.routing_tree.insert(key, val)
		self.routing_tree.insert('/api/monkey/test/extension', {'GET':self.testHandle})

	def testHandle(self):
		print('main handler')
	def handler(thisSchema):
		def decorator(func):
			@wraps(func)
			def wrapper(self, *args, **kwargs):
				print("we are in a wrapper")
				print(thisSchema)
				data = json.loads(self.request['data'])
				params = data.get('params')
				schema = thisSchema
				if not params:
					params = self.parameters
				hasParams, validTypes = self.validateParameters(data, schema)

				if hasParams and validTypes:
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

	def getAppArchitecture(self):
		data = {
			'name': 'Application Architecture',
			'id': 'app.architecture',
			'description': 'The architecture of the compile. Generally 32 or 64 bit.',
			'built-in': True,
			'data': {
					'value': app.architecture,
					'type': 'int'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/v1/app/architecture'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppBuild(self):
		data = {
			'name': 'Application Build',
			'id': 'app.build',
			'description': 'Application build number.',
			'built-in': True,
			'data': {
					'value': app.build,
					'type': 'str'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/v1/app/build'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppLaunchTime(self):
		data = {
			'name': 'Application Launch Time',
			'id': 'app.launchTime',
			'description': 'Total time required to launch and begin playing the toe file, measured in seconds.',
			'built-in': True,
			'data': {
					'value': app.launchTime,
					'type': 'float'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/v1/app/launchTime'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppStartTimestamp(self):
		timestamp = op('records')['startTimestamp', 'value'].val
		data = {
			'name': 'Application Start Time',
			'id': 'custom.app.startTimestamp',
			'description': 'UNIX timestamp recorded when the application launches.',
			'built-in': False,
			'data': {
					'value': timestamp,
					'type': 'float'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/v1/app/startTimestamp'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppOSName(self):

		data = {
			'name': 'Application OS Name',
			'id': 'app.osName',
			'description': 'The operating system name.',
			'built-in': True,
			'data': {
					'value': app.osName,
					'type': 'str'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/v1/app/osName'
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
					'href': self.rel_prefix + 'api/v1/app/power'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	@handler(schemas['put_app_power'])
	def putAppPowerN(self):
		data = json.loads(self.request['data'])
		power = data['state']
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

	@handler(schemas['put_app_power'])
	def putAppPower(self):
		data = json.loads(self.request['data'])
		# data_schema = schemas['put_app_power']
		# hasParams, validTypes = self.validateParameters(data, data_schema)
		# if hasParams and validTypes:

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
		# else:
		# 	self.formatResponse(400, 'Bad Format', {})

	def getAppProduct(self):
		data = {
			'name': 'Application Product',
			'id': 'app.product',
			'description': 'Type of executable the project is running under.',
			'built-in': True,
			'data': {
					'value': app.product,
					'type': 'str'
			},
			'links': [
				{
					'rel': 'self',
					'href': self.rel_prefix + 'api/v1/app/product'
				}
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
					'href': self.rel_prefix + 'api/v1/app/version'
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
		# data_schema = schemas['put_app_play']
		# hasParams, validTypes = self.validateParameters(data, data_schema)

		# if hasParams and validTypes:
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
		# else:
		# 	self.formatResponse(400, 'Bad Format', {})

#################### PROJECT ##########################
	def getProjectName(self):
		data = {
			'name': 'Project Name',
			'id': 'project.name',
			'description': 'The filename under which the project is saved.',
			'built-in': True,
			'data': {
					'value': project.name,
					'type': 'str'
			}
		}
		self.formatResponse(200, 'OK', data)

	def getProjectPaths(self):
		data = {
			'name': 'Project Paths',
			'id': 'project.paths',
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
			'id': 'project.cookRate',
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
		# data_schema = schemas['put_project_cookRate']
		# hasParams, validTypes = self.validateParameters(data, data_schema)
		# if hasParams and validTypes:
		rate = data['rate']
		project.cookRate = rate
		data = {
			'success': {
				'name': 'Project Cook Rate',
				'id': 'project.cookRate',
						'data': {
							'value': project.cookRate,
							'type': 'float'
						}
			}
		}
		self.formatResponse(200, 'OK', data)
		# else:
		# 	self.formatResponse(400, 'Bad Format', {})

	def getProjectSaveVersion(self):
		data = {
			'name': 'Project Save Version',
			'id': 'project.saveVersion',
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
			'id': 'project.saveBuild',
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
			'id': 'project.realTime',
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
			'success': {
				'name': 'Project Real Time',
				'id': 'project.realTime',
						'data': {
							'value': project.realTime,
							'type': 'bool'
						}
			}
		}
		self.formatResponse(200, 'OK', data)

	def getProjectPerformOnStart(self):
		data = {
			'name': 'Project Perform on Start',
			'id': 'project.performOnStart',
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
			'success': {
				'name': 'Project Perform on Start',
				'id': 'project.performOnStart',
						'data': {
							'value': project.performOnStart,
							'type': 'bool'
						}
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
			'id': 'sysinfo.numCPUs',
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
			'id': 'sysinfo.ram',
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
			'name':'UI Master Volume',
			'id':'ui.masterVolume',
			'description':'',
			'data':{
				'value':ui.masterVolume,
				'type':'float'
			}
		}
		self.formatResponse(200, 'OK', data)

	@handler(schemas['put_ui_masterVolume'])
	def putUIMasterVolume(self):
		data = json.loads(self.request['data'])

		volume = data['volume']
		ui.masterVolume = volume
		data = {
			'success': {
				'name': 'UI Master Volume',
				'id': 'ui.masterVolume',
						'data': {
							'value': ui.masterVolume,
							'type': 'float'
						}
			}
		}
		self.formatResponse(200, 'OK', data)

	def getMonitors(self):
		monitorsData = []
		for m in range(len(monitors)):
			thisMonitor = {
				'name': monitors[m].displayName,
				'description': monitors[m].description,
				'index': m
			}
			monitorsData.append(thisMonitor)
		data = {
			'name': 'Monitors',
			'id': 'monitors',
			'description': 'Monitors connected to machine',
			'built-in': True,
			'data': {
					'value': monitorsData,
					'type': 'list'
			}
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
			'success':'I will format later'
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
		self.formatResponse(200, 'OK', data)

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
		# params_schema = schemas['get_op_name']
		# hasParams, validTypes = self.validateParameters(params, params_schema)
		# if hasParams and validTypes:
		path = params.get('path') or int(params.get('id'))
		print(path)
		operator = op(path)
		print(operator)
		if operator:
			name = operator.name
			data = {
				'name': 'Operator Name',
				'id': 'op.name',
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
		# else:
		# 	self.formatResponse(400, 'Bad Request', {})

	@handler(schemas['put_op_name'])
	def putOpName(self):
		data = json.loads(self.request['data'])
		# data_schema = schemas['put_op_name']
		# hasParams, validTypes = self.validateParameters(data, data_schema)

		# if hasParams and validTypes:
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
		self.formatResponse(200,'OK', data)
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
		# if not 'path' in parameters.keys():
		# 	self.formatMissingParamMessage('path')
		# 	return -1
		# else:
		path = params.get('path') or int(params.get('id'))
		operator = op(path)
		if operator:
			# tags = op(path).tags
			_tags = [tag for tag in operator.tags]
			operatorId = op(path).id
			operatorName = op(path).name
			data = {
				'name': f'Operator {operatorId} Tags',
				'id': f'op.tags',
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
		data = json.loads(self.request['data'])

		path = data.get('path') or int(data.get('id'))
		tags = data['tags']

		operator = op(path)
		if operator:
			for tag in tags:
				operator.tags.add(tag)
			data = {'message':'Format this!!'}
			self.formatResponse(200, 'OK', data)
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

		handler, params = self.routing_tree.find(uri, method)
		print(handler, params)
		if params:
			self.parameters = params

		#handler()
		print('uri')
		if uri.split('/')[2] == 'monkey':
			print('monkey')
			handler(self)
		else:
			handler()

		return self.response

	def format500(self, data=None, error = 'unknown'):
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
	
	def InsertRoute(self, url: str, handlers:dict):
		self.url = url
		url = '/api/monkey' + url
		self.routing_tree.insert(url, handlers)


		# no reason to return, because we are passing the self.response dict
