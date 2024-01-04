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
	routing_tree = ttrie.Trie()
	def __init__(self, thisComp):
		self.thisComp = thisComp
		self.itrap_port = thisComp.par.Port
		self.ip_address = thisComp.par.Ipaddress
		print(thisComp)
		self.routing_table = {
			"GET /api/v1/app/architecture": self.getAppArchitecture,
			"GET /api/v1/app/build": self.getAppBuild,
			"GET /api/v1/app/launchTime": self.getAppLaunchTime,
			"GET /api/v1/app/startTimestamp":self.getAppStartTimestamp,
			"GET /api/v1/app/osName": self.getAppOSName,
			"GET /api/v1/app/power": self.getAppPower,
			"PUT /api/v1/app/power": [self.putAppPowerN, schemas['put_app_power']],
			"GET /api/v1/app/product": self.getAppProduct,
			"GET /api/v1/app/version": self.getAppVersion,
			"GET /api/v1/app/play": self.getAppPlay,
			"PUT /api/v1/app/play": self.putAppPlay,
			"GET /api/v1/project/name": self.getProjectName,
			"GET /api/v1/project/saveVersion": self.getProjectSaveVersion,
			"GET /api/v1/project/saveBuild": self.getProjectSaveBuild,
			"GET /api/v1/project/saveTime": self.getProjectSaveTime,
			"GET /api/v1/project/saveOSName": self.getProjectSaveOSName,
			"GET /api/v1/project/saveOSVersion": self.getProjectSaveOSVersion,
			"GET /api/v1/project/paths": self.getProjectPaths,
			"GET /api/v1/project/cookRate": self.getProjectCookRate,
			"PUT /api/v1/project/cookRate": self.putProjectCookRate,
			"GET /api/v1/project/realTime": self.getProjectRealTime,
			"PUT /api/v1/project/realTime": self.putProjectRealTime,
			"GET /api/v1/project/performOnStart": self.getProjectPerformOnStart,
			"PUT /api/v1/project/performOnStart": self.putProjectPerformOnStart,
			"POST /api/v1/project/load": self.postProjectLoad,
			"POST /api/v1/project/save": self.postProjectSave,
			"POST /api/v1/project/quit": self.postProjectQuit,
			"GET /api/v1/sysinfo/numCPUs": self.getSysInfoNumCpus,
			"GET /api/v1/sysinfo/ram": self.getSysInfoRAM,
			"GET /api/v1/ui/masterVolume": self.getUIMasterVolume,
			"PUT /api/v1/ui/masterVolume": self.putUIMasterVolume,
			"GET /api/v1/monitors": self.getMonitors,
			"POST /api/v1/monitors/refresh": self.postMonitorsRefresh,
			"GET /api/v1/op": self.getOp,
			"POST /api/v1/op": self.postOp,
			"DELETE /api/v1/op": self.deleteOp,
			"GET /api/v1/op/opIdMap": self.getOpIdMap,
			"GET /api/v1/op/id": self.getOpID,
			"GET /api/v1/op/name": self.getOpName,
			"PUT /api/v1/op/name": self.putOpName,
			"GET /api/v1/op/storage": self.getOpStorage,
			"GET /api/v1/op/tags": self.getOpTags,
			"POST /api/v1/op/tags": self.postOpTags,
			"DELETE /api/v1/op/tags": self.deleteOpTags,
			"GET /api/v1/op/par": self.getOpPar,
			"PUT /api/v1/op/par": self.putOpPar,
		}

	def TestHandler(func):
		@wraps(func)
		def wrapper(self, *args, **kwargs):
			data = json.loads(self.request['data'])
			params = data.get('params')
			schema = args[0]
			if not params:
				params = self.parameters
			hasParams, validTypes = self.validateParameters(data, schema)

			if hasParams and validTypes:
				func(self,*args, **kwargs)
			else:
				self.formatResponse(400, 'Bad Request', {})
		return wrapper
	
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
				'path':path,
				'id':_id
			}
			operator_id_map[name] = _map

		return operator_id_map
	
	def quit(self):
		project.quit(force=True)

	def formatMissingParamMessage(self, param):
		data = {
			'error':{
				'message':f'KeyError: Missing required parameter {param}.'
			}
		}
		self.formatResponse(400, 'Bad Request', data)
		return -1

	def formatTypeErrorMessage(self, param, _type):
		data = {
			'error':{
				'message':f'TypeError: "{param}" must be type {_type}'
			}
		}
		self.formatResponse(400, 'Bad Request', data)
		return -1
	
	def validateParameters(self, pars: dict, schema):
		included_pars = pars.keys()
		expected_pars = schema['parameters']
		required_pars = schema['required']

		hasRequired = True

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
				else:
					validType = validType and (expected_type == type(val))

		return hasRequired, validType

	def getAppArchitecture(self):
		data = {
			'name':'Application Architecture',
			'id':'app.architecture',
			'description':'The architecture of the compile. Generally 32 or 64 bit.',
			'built-in':True,
			'data':{
				'value':app.architecture,
				'type':'int'
			},
			'links':[
				{
					'rel':'self',
					'href':self.rel_prefix + 'api/v1/app/architecture'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppBuild(self):
		data = {
			'name':'Application Build',
			'id':'app.build',
			'description':'Application build number.',
			'built-in':True,
			'data':{
				'value':app.build,
				'type':'str'
				},
			'links':[
				{
					'rel':'self',
					'href':self.rel_prefix + 'api/v1/app/build'
				}
			]
		}
		self.formatResponse(200, 'OK', data)
	
	def getAppLaunchTime(self):
		data = {
			'name':'Application Launch Time',
			'id':'app.launchTime',
			'description':'Total time required to launch and begin playing the toe file, measured in seconds.',
			'built-in':True,
			'data':{
				'value':app.launchTime,
				'type':'float'
				},
			'links':[
				{
					'rel':'self',
					'href':self.rel_prefix + 'api/v1/app/launchTime'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppStartTimestamp(self):
		timestamp = op('records')['startTimestamp', 'value'].val
		data = {
			'name':'Application Start Time',
			'id':'custom.app.startTimestamp',
			'description':'UNIX timestamp recorded when the application launches.',
			'built-in':False,
			'data':{
				'value':timestamp,
				'type':'float'
				},
			'links':[
				{
					'rel':'self',
					'href':self.rel_prefix + 'api/v1/app/startTimestamp'
				}				
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppOSName(self):
		
		data = {
			'name':'Application OS Name',
			'id':'app.osName',
			'description':'The operating system name.',
			'built-in':True,
			'data':{
				'value':app.osName,
				'type':'str'
				},
			'links':[
				{
					'rel':'self',
					'href':self.rel_prefix + 'api/v1/app/osName'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppPower(self):

		data = {
			'name':'Application Power State',
			'id':'app.power',
			'description':'Processing state of the application. This has a greater effect than simply pausing or stopping the playbar.',
			'data':{
				'value':app.power,
				'type':'bool'
				},
			'links':[
				{
					'rel':'self',
					'href':self.rel_prefix + 'api/v1/app/power'
				}
			]
		}
		self.formatResponse(200, 'OK', data)

	@TestHandler
	def putAppPowerN(self, schema):
		data = json.loads(self.request['data'])
		power = data['state']
		app.power = power

		data = {
			'success':{
				'name':'Application Power',
				'id':'app.power',
				'data':{
					'value':app.power,
					'type':'bool'
				}
			}
		}

		self.formatResponse(200, 'OK', data)



	def putAppPower(self):
		data = json.loads(self.request['data'])
		data_schema = schemas['put_app_power']
		hasParams, validTypes = self.validateParameters(data, data_schema)
		if hasParams and validTypes:
			# if not 'state' in data.keys():
			# 	self.formatMissingParamMessage('state')
			# 	return -1
			
			power = data["state"]
			# if type(power) != bool:
			# 	self.formatTypeErrorMessage('power', 'bool')
			# 	return -1

			app.power = power

			data = {
				'success':{
					'name':'Application Power',
					'id':'app.power',
					'data':{
						'value':app.power,
						'type':'bool'
					}
				}
			}

			self.formatResponse(200, 'OK', data)
		else:
			self.formatResponse(400, 'Bad Format', {})

	def getAppProduct(self):
		data = {
			'name':'Application Product',
			'id':'app.product',
			'description':'Type of executable the project is running under.',
			'built-in':True,
			'data':{
				'value':app.product,
				'type':'str'
				},
			'links':[
				{
					'rel':'self',
					'href':self.rel_prefix + 'api/v1/app/product'
				}				
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppVersion(self):
		data = {
			'name':'Application Version',
			'id':'app.version',
			'description':'Application version number.',
			'built-in':True,
			'data':{
				'value':app.version,
				'type':'str'
				},
			'links':[
				{
					'rel':'self',
					'href':self.rel_prefix + 'api/v1/app/version'
				}				
			]
		}
		self.formatResponse(200, 'OK', data)

	def getAppPlay(self):
		data = {
			'name':'Application Transport State',
			'id':'custom.app.play',
			'description':'Indicates whether the application is playing or stopped.',
			'built-in':False,
			'data':{
				'value':op('/local/time').play,
				'type':'bool'
			}
		}

		self.formatResponse(200, 'OK', data)

	def putAppPlay(self):
		data = json.loads(self.request['data'])
		data_schema = schemas['put_app_play']
		hasParams, validTypes = self.validateParameters(data, data_schema)
		# if not 'play' in data.keys():
		# 	self.formatMissingParamMessage('play')
		# 	return -1
		# else:
		if hasParams and validTypes:
			play = data['play']
			# if type(play) != bool:
			# 	self.formatTypeErrorMessage('play', 'bool')
			# 	return -1
			# else:
			op("/local/time").play = play
			data = {
				'sucess':{
					'name':'Application Transport State',
					'id':'custom.app.play',
					'data':{
						'value':op("/local/time").play,
						'type':{
							"oneOf":[
								'boolean',
								'integer'
							]
						}
					}
				}
			}
			self.formatResponse(200, 'OK', data)
		else:
			self.formatResponse(400, 'Bad Format', {})

#################### PROJECT ##########################
	def getProjectName(self):
		data = {
			'name':'Project Name',
			'id':'project.name',
			'description':'The filename under which the project is saved.',
			'built-in':True,
			'data':{
				'value':project.name,
				'type':'str'
			}
		}
		self.formatResponse(200, 'OK', data)

	def getProjectPaths(self):
		data = {
			'name':'Project Paths',
			'id':'project.paths',
			'description':'A dictionary which can be used to define URL-syntax path prefixes, enabling you to move your media to different locations easily.',
			'built-in':True,
			'data':{
				'value':project.paths,
				'type':'dict'
			}
		}
		self.formatResponse(200, "OK", data)

	def postProjectPaths(self):
		pass
	def putProjectPaths(self):
		pass
	def getProjectCookRate(self):
		data = {
			'name':'Project Cook Rate',
			'id':'project.cookRate',
			'description':'The maximum number of frames processed each second.',
			'built-in':True,
			'data':{
				'value':project.cookRate,
				'type':'float'
			}
		}
		self.formatResponse(200, "OK", data)

	def putProjectCookRate(self):
		data = json.loads(self.request['data'])
		data_schema = schemas['put_project_cookRate']
		hasParams, validTypes = self.validateParameters(data, data_schema)
		if hasParams and validTypes:
			rate = data['rate']
			project.cookRate = rate
			data = {
				'success':{
					'name':'Project Cook Rate',
					'id':'project.cookRate',
					'data':{
						'value':project.cookRate,
						'type':'float'
					}
				}
			}
			self.formatResponse(200, 'OK', data)
		else:
			self.formatResponse(400, 'Bad Format', {})
		# if not 'rate' in data.keys():
		# 	self.formatMissingParamMessage('rate')
		# 	return -1
		# else:
		# 	rate = data['rate']
		# 	_typeFloat = type(rate) == float
		# 	_typeInt = type(rate) == int

		# 	if not (_typeFloat or _typeInt):
		# 		self.formatTypeErrorMessage('rate', 'float OR int')
		# 		return -1
		# 	else:
		# 		project.cookRate = rate
		# 		data = {
		# 			'success':{
		# 				'name':'Project Cook Rate',
		# 				'id':'project.cookRate',
		# 				'data':{
		# 					'value':project.cookRate,
		# 					'type':'float'
		# 				}
		# 			}
		# 		}
		# 		self.formatResponse(200, 'OK', data)

	def getProjectSaveVersion(self):
		data = {
			'name':'Project Save Version',
			'id':'project.saveVersion',
			'description':'The App version number when the project was last saved.',
			'built-in':True,
			'data':{
				'value':project.saveVersion,
				'type':'str'
			}
		}

		self.formatResponse(200, 'OK', data)

	def getProjectSaveBuild(self):
		data = {
			'name':'Project Save Build',
			'id':'project.saveBuild',
			'description':'The App build number when the project was last saved.',
			'built-in':True,
			'data':{
				'value':project.saveBuild,
				'type':'str'
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
			'name':'Project Real Time',
			'id':'project.realTime',
			'description':'Realtime cooking state. When True, frames may be skipped in order to maintain the cookRate.',
			'built-in':True,
			'data':{
				'value':project.realTime,
				'type':'bool'
			}
		}
		self.formatResponse(200, 'OK', data)
		
	def putProjectRealTime(self):
		data = json.loads(self.request['data'])
		if not 'realTime' in data.keys():
			self.formatMissingParamMessage('realTime')
			return -1
		else:
			realTime = data['realTime']
			if type(realTime) != bool:
				self.formatTypeErrorMessage('realTime', 'bool')
			else:
				project.realTime = realTime
				data = {
					'success':{
						'name':'Project Real Time',
						'id':'project.realTime',
						'data':{
							'value':project.realTime,
							'type':'bool'
						}
					}
				}
				self.formatResponse(200, 'OK', data)

	def getProjectPerformOnStart(self):
		print('received')
		data = {
			'name':'Project Perform on Start',
			'id':'project.performOnStart',
			'description':'If True, project starts in perform mode.',
			'built-in':True,
			'data':{
				'value':project.performOnStart,
				'type':'bool'
			}
		}
		self.formatResponse(200, 'OK', data)

	def putProjectPerformOnStart(self):
		data = json.loads(self.request['data'])
		if not 'performOnStart' in data.keys():
			self.formatMissingParamMessage('performOnStart')
			return -1
		else:
			performOnStart = data['performOnStart']
			_typeBool = type(performOnStart) == bool
			_typeInt = type(performOnStart) == int
			if not (_typeBool or _typeInt):
				self.formatTypeErrorMessage('performOnStart', 'bool or int')
			else:
				project.performOnStart = performOnStart
				data = {
					'success':{
						'name':'Project Perform on Start',
						'id':'project.performOnStart',
						'data':{
							'value':project.performOnStart,
							'type':'bool'
						}
					}
				}
				self.formatResponse(200, 'OK', data)

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

	def postProjectSave(self):
		data = json.loads(self.request['data'])
		if 'path' in data.keys():
			path = data['path']
			pathType = type(path) == str
			if not pathType:
				self.formatTypeErrorMessage('path', 'str')
				return -1
			project.save(path) # what if this returns an error?
		else:
			project.save()

		self.formatResponse(204, 'No Content', {})

	def postProjectQuit(self):
		self.quit()
		data = {}
		self.formatResponse(204, 'No Content', data)
	def getSysInfoNumCpus(self):
		data = {
			'name':'Sysinfo CPU Count',
			'id':'sysinfo.numCPUs',
			'description':'',
			'data':{
				'value':sysinfo.numCPUs,
				'type':int
			}
		}

		self.formatResponse(200, 'OK', data)

	def getSysInfoRAM(self):
		data = {
			'name':'Sysinfo RAM',
			'id':'sysinfo.ram',
			'description':'',
			'data':{
				'value':sysinfo.ram,
				'type':int
			}
		}
		self.formatResponse(200, 'OK', data)

	def getSysInfoRes(self):
		return
	def getSysInfoNumMonitors(self):
		return
	def getUIMasterVolume(self):
		data = {
			'success':{
				'data':ui.masterVolume
			}
		}
		self.formatResponse(200, 'OK', data)

	def putUIMasterVolume(self):
		data = json.loads(self.request['data'])
		data_schema = schemas['put_ui_masterVolume']
		hasParams, validTypes = self.validateParameters(data, data_schema)

		if hasParams and validTypes:
			volume = data['volume']
			ui.masterVolume = volume
			data = {
				'success':{
					'name':'UI Master Volume',
					'id':'ui.masterVolume',
					'data':{
						'value':ui.masterVolume,
						'type':'float'
					}
				}
			}
			self.formatResponse(200, 'OK', data)
		else:
			self.formatResponse(400, 'Bad Request', {})		
			
		# if not 'volume' in data.keys():
		# 	self.formatMissingParamMessage('volume')
		# else:
		# 	volume = data['volume']
		# 	_typeInt = type(volume) == int
		# 	_typeFloat = type(volume) == float
			
		# 	if not (_typeInt or _typeFloat):
		# 		self.formatTypeErrorMessage('volume', 'int or float')
		# 		return -1
		# 	_inBounds = volume >= 0 and volume <= 1
		# 	if not _inBounds:
		# 		data = {
		# 			'error':{
		# 				'message':'RangeError: Volume must be between 0 and 1'
		# 			}
		# 		}
		# 		self.formatResponse(400, 'Bad Request', data)
		# 		return -1
		# 	ui.masterVolume = volume
		# 	data = {
		# 		'success':{
		# 			'data':ui.masterVolume
		# 		}
		# 	}
		# 	self.formatResponse(200, 'OK', data)
	def getMonitors(self):
		monitorsData = []
		for m in range(len(monitors)):
			thisMonitor = {
				'name':monitors[m].displayName,
				'description':monitors[m].description,
				'index':m
			}
			monitorsData.append(thisMonitor)
		data = {
			'name':'Monitors',
			'id':'monitors',
			'description':'Monitors connected to machine',
			'built-in':True,
			'data':{
				'value':monitorsData,
				'type':'list'
			}
		}
		self.formatResponse(200, 'OK', data)

	def postMonitorsRefresh(self):
		return
############# OPERATORS ############
	def unpackOperatorPointerParam(self, params):
		_hasPath = 'path' in params.keys()
		_hasId = 'id' in params.keys()
		if not (_hasPath or _hasId):
			self.formatMissingParamMessage('path or id')
			return False
		
		path = None
		if _hasPath:
			path = params['path']
		elif _hasId:
			path = params['id']
		
		operator = op(path)
		if not operator:
			data = {
				'error':{
					f'NoneType: operator {path} does not exist.'
				}
			}
			self.formatResponse(404, 'Not Found', data)
			return False
		
		return path

	def getOp(self):

		hasPath = 'path' in self.parameters.keys()
		hasAttribute = 'attribute' in self.parameters.keys()
		data = {
			'error':'missing parameters'
		}
		if not (hasPath and hasAttribute):
			self.formatResponse(400, 'Missing Parameters',data)
	def postOp(self):
		data = json.loads(self.request['data'])
		data_schema = schemas.schema['post_op']
		hasParams, validTypes = self.validateParameters(parameters, data_schema)
		
		if hasParams and validTypes:
			name = data['name']
			_type = data['type']
			parent = data['parent']
			newOp = op(parent).create(_type, name)
			
			# need to check if parent exists
			data = {
				'name-space':'Operator',
				'id-space':'op',
				'data':{
					'name':newOp.name,
					'id':newOp.id,
					'path':newOp.path,
					'type':{
						'family':newOp.family,
						'label':newOp.label,
						'type':newOp.type,
						'subType':newOp.subType,
						'OPType':newOp.OPType

					},
					'time':newOp.time.path,
					'flags':[
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
		else:
			self.formatResponse(400, 'Bad Request', {})
	def deleteOp(self):
		data = json.loads(self.request['data'])
		data_schema = schemas['delete_op']
		hasParams, validTypes = self.validateParameters(data, data_schema)

		if hasParams and validTypes:
			path = data.get('path') or data.get('id')
			operator = op(path)
			if not operator:
				data = {
					'error':{
						f'NoneType: operator {path} does not exist.'
					}
				}
				self.formatResponse(404, 'Not Found', data)
			else:
				op(path).destroy()
				self.formatResponse(204, 'No Content')
		else:
			self.formatResponse(400, 'Bad Request', {})

		# _hasPath = 'path' in data.keys(data)
		# _hasId = 'id' in data.keys()
		# if not (_hasPath or _hasId):
		# 	self.formatMissingParamMessage('path or id')
		# 	return -1
		# path = None
		# if _hasPath:
		# 	path = data['path']
		# elif _hasId:
		# 	path = data['id']
		# operator = op(path)
		# if not operator:
		# 	data = {
		# 		'error':{
		# 			f'NoneType: operator {path} does not exist.'
		# 		}
		# 	}
		# 	self.formatResponse(404, 'Not Found', data)
		# else:
		# 	op(path).destroy()
		# 	self.formatResponse(204, 'No Content')
	def getOpIdMap(self):
		opIdMap = self.mapOperators()
		
		data = {
			'name':'Operator Id Map',
			'id':'op("mapped_operator_ids")',
			'description':'Dictionary mapping absolute operator paths to their unique ID\'s. Only contains operators that have been explicitly configured.',
			'built-in':False,
			'data':{
				'value':opIdMap,
				'type':'dict'
			}
		}
		self.formatResponse(200, 'OK', data)

	def getOpID(self):
		params = self.parameters
		params_schema = schemas['get_op_id']
		hasParams, validTypes = self.validateParameters(params, params_schema)
		path = params['path']
		operator = op(path)
		if hasParams and validTypes:
			if operator:
				_id = operator.id
				data = {
					'name':'Operator ID',
					'id':'op.id',
					'description':'Unique integer identifier.',
					'built-in':True,
					'data':{
						'value':_id,
						'type':'int'	
					}
				}
				self.formatResponse(200, 'OK', data)
			else:
				self.formatResponse(404, 'Not Found')
		else:
			self.formatResponse(400, 'Bad Request', {})
	
	def getOpName(self):
		params = self.parameters
		params_schema = schemas['get_op_name']
		hasParams, validTypes = self.validateParameters(params, params_schema)
		if hasParams and validTypes:
			path = params.get('path') or params.get('id')
			operator = op(path)
			if operator:
				name = operator.name
				data = {
					'name':'Operator Name',
					'id':'op.name',
					'description':'',
					'built-in':True,
					'data':{
						'value':name,
						'type':'str'
					}
				}
			
				self.formatResponse(200, 'OK', data)
			else:
				self.formatResponse(404, 'Resource Not Found', {})
		else:
			self.formatResponse(400, 'Bad Request', {})

		# path = self.unpackOperatorPointerParam(parameters)
		# if path:
		# 	name = op(path).name
		# 	data = {
		# 		'name':'Operator Name',
		# 		'id':'op.name',
		# 		'description':'',
		# 		'built-in':True,
		# 		'data':{
		# 			'value':name,
		# 			'type':'str'
		# 		}
		# 	}
		
		# 	self.formatResponse(200, 'OK', data)
	
	def putOpName(self):
		data = json.loads(self.request['data'])
		data_schema = schemas['put_op_name']
		hasParams, validTypes = self.validateParameters(data, data_schema)
		
		if hasParams and validTypes:
			path = data.get('path') or data.get('id')
			name = data.get('name')
			operator = op(path)
			if not operator:
				self.formatResponse(404, 'Resource Not Found', {})
				return -1
			operator.name = name
			
			data = {
				'success':{
					'name':'Operator',
					'id':'op.name'
				}
			}

	def getOpStorage(self):
		params = self.parameters
		params_schema = schemas['get_op_storage']
		hasParams, validTypes = self.validateParameters(params_schema, params)

		if hasParams and validTypes:
			path = params['path']
			operator = op(path)
			if not operator:
				self.formatResponse(404, 'Resource Not Found', {})
				return -1
			if not hasattr(operator, 'storage'):
				self.formatResponse(422, 'Unprocessable Content', {})
				return -1

			data = {
				'name':'Operator Storage',
				'id':'op.storage',
				'description':'',
				'data':{
					'value':operator.storage,
					'type':'dict'
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
					'error':{
						'message':f'EXCEPTION: {str(e)}'
					}
				}
			finally:
				self.formatResponse(code, message, data)
		else:
			self.formatResponse(400, 'Bad Format', {})
			
		# if not 'path' in data.keys():
		# 	self.formatMissingParamMessage('path')
		# 	return -1
		# else:
		# 	path = data['path']
		# 	if hasattr(op(path), 'storage'):
		# 		storage = op(path).storage
		# 		data = {}
		# 		try:
		# 			data = json.dumps(storage)
		# 			code = 200
		# 			message = 'OK'
		# 		except Exception as e:
		# 			data = {
		# 				'error':{
		# 					'message':f'EXCEPTION: {str(e)}'
		# 				}
		# 			}
		# 			code = 500
		# 			message = 'Internal Server Error'
		# 		finally:
		# 			self.formatResponse(code, message, data)
		# 	else:
		# 		data = {
		# 			'error':{
		# 				'message':f'EXCEPTION: {path} does not support storage'
		# 			}
		# 		}
		# 		message = self.formatResponse(422, 'Unprocessable Content', data)

	def getOpTags(self):
		parameters = json.loads(self.parameters)
		if not 'path' in parameters.keys():
			self.formatMissingParamMessage('path')
			return -1
		else:
			path = parameters['path']
			operator = op(path)
			if operator:
				tags = op(path).tags
				operatorId = op(path).id
				operatorName = op(path).name
				data = {
					'name':f'Operator {operatorId} Tags',
					'id':f'op({operatorId}).tags',
					'description':'',
					'data':{
						'value':tags,
						'type':'set',
						'items':{
							'type':'str'
						}
					},
					'operator_name':operatorName,
					'operator_id':operatorId
				}
				self.formatResponse(200, 'OK', data)
			else:
				data = {
					'error': f'NoneTypeError: op("{path}") does not exist.'
				}
				self.formatResponse(404, 'Resource Not Found', data)
	def postOpTags(self):
		data = json.loads(self.request['data'])
		_pathExists = 'path' in data.keys()
		_tagsExist = 'tags' in data.keys()

		if not (_pathExists and _tagsExist):
			self.formatMissingParamMessage('[path, tags]')
		else:
			path = data['keys']
			tags = data['tags']
			_pathIsStr = type(path) == str
			_tagsIsList = type(tags) == list

			if not (_pathIsStr and _tagsIsList):
				self.formatTypeErrorMessage('[path, tags]', '[str, list]')
			else:
				operator = op(path)
				if operator:
					for tag in tags:
						operator.tags.add(tag)
				else:
					data = {
						'error': f'NoneTypeError: op("{path}") does not exist.'
					}
					self.formatResponse(404, 'Resource Not Found', data)
	def deleteOpTags(self):
		data = json.loads(self.request['data'])
		path = data['path']
		tags = data['tags']
		for tag in tags:
			op(path).tags.remove(tag)
		
		self.formatResponse(204, 'No Content')

	def getOpPar(self):
		parameters = self.parameters
		path = parameters['path']
		param = parameters['par']
		value = op(path).par[param].val
		data = {
			'data':value
		}
		self.formatResponse(200, 'OK', data)
		
	def putOpPar(self):
		parameters = self.parameters
		path = parameters['path']
		param = parameters['par']
		value = parameters['val']
		op(path).par[param].val = value
		data = {
			'success':True
		}
		self.formatResponse(200, 'OK', data)

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

	def parseOpURI(uri):
		# extract name and attribute (or par) from uri
		op_name = uri[2]
		attrib = uri[-1]

		# strip op_name and attrib from uri and join back into path
		uri = uri[:2] + uri[3:-1]
		uri = "/".join(uri)

		return [op_name,attrib,uri]

	def formatResponse(self, code, reason, data={}):
		try:
			data = json.dumps(data)
		except Exception as e:
			data = {
				'error':{
					'message':f'Server encountered an exception while encoding return data.',
					'exception':str(e)
				}
			}
			code = 500
			reason = 'Internal Server Error'
		finally:
			self.response["statusCode"] = code
			self.response["statusReason"] = reason
			self.response["data"] = data
	
	def formatSuccess(self, data):

		self.response['statusCode'] = 200
		self.response['statusReason'] = 'OK'
		responseData = {
			'success':True,
			'data':data
		}
		data = json.dumps(responseData)

		self.response['data'] = data


		# no reason to return, because we are passing the self.response dict

