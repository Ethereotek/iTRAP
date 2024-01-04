import unittest
components = {

	'path': {
		'path': {
			'type': str
		}
	},
	'path&id': {
		'path': {
			'type': str
		},
		'id': {
			'type': int
		}
	},
	'tag_params':{
		'path': {
			'type': str
		},
		'id': {
			'type': int
		},
		'tags':{
			'type':list
		}       
	}
}
schemas = {
	'put_app_power': {
		'parameters': {
			'state': {
				'type': (bool, int)
			}
		},
		'required': ['state']
	},
	'put_app_play': {
		'parameters': {
			'play': {
				'type': (bool, int)
			}
		},
		'required': ['play']
	},
	'put_project_cookRate': {
		'parameters': {
			'rate': {
				'type': (int, float)
			}
		},
		'required': ['rate']
	},
	'put_project_realTime': {
		'parameters': {
			'realTime': {
				'type': (int, bool)
			}
		},
		'required': ['realTime']
	},
	'put_project_performOnStart': {
		'parameters': {
			'performOnStart': {
				'type': (int, bool)
			}
		},
		'required': ['performOnStart']
	},
	'post_project_load': {
		'parameters': components['path'],
		'required': []
	},
	'post_project_save': {
		'parameters': components['path'],
		'required': []
	},
	'put_ui_masterVolume': {
		'parameters': {
			'volume': {
				'type': (int, float)
			}
		},
		'required': ['volume']
	},
	'get_op': {
		'parameters': components['path&id'],
		'required': [['path', 'id']]
	},
	'post_op': {
		'parameters': {
			'name': {
				'type': str
			},
			'type': {
				'type': str
			},
			'parent': {
				'type': str
			}
		},
		'required': [
			'name',
			'type',
			'parent'
		]
	},
	'delete_op': {
		'parameters': components['path&id'],
		'required': [['path', 'id']]
	},
	'get_op_id': {
		'parameters': components['path'],
		'required': ['path']
	},
	'get_op_name': {
		'parameters': components['path&id'],
		'required': [['path', 'id']]
	},
	'put_op_name': {
		'parameters': {
			'path': {
				'type': str
			},
			'id': {
				'type': int
			},
			'name': {
				'type': str
			}
		},
		'required': [
			'name',
			['path', 'id']
		]
	},
	'get_op_storage': {
		'parameters': components['path&id'],
		'required': [['path', 'id']]
	},
	'get_op_tags': {
		'parameters': components['path&id'],
		'required':[['path', 'id']]
	},
	'post_op_tags':{
		'parameters':components['tag_params'],
		'required':[
			['path', 'id'],
			'tags'
		]
	},
	'delete_op_tags':{
		'parameters':components['tag_params'],
		'required':[
			['path', 'id'],
			'tags'
		]
	},
	'get_op_par':{
		'parameters':{
			'path':{
				'type':str
			},
			'id':{
				'type':str
			},
			'name':{
				'type':str
			}
		},
		'required':[
			['path', 'id'],
			'name'
		]
	},
	'put_op_par':{
		'parameters':{
			'path':{
				'type':str
			},
			'id':{
				'type':str
			},
			'par':{
				'type':str
			},
			'val':{
				'type':str
			}
		},
		'required':[
			['path', 'id'],
			'par',
			'val'
		]
	},
	'get_named_op':{
		'parameters':{
			'name':{
				'type':str
			}
		},
		'required':['name']
	},
	'get_named_op_attribute':{
		'parameters':{
			'name':{
				'type':str
			},
			'attribute':{
				'type':str
			}
		},
		'required':['name', 'attribute']
	},
	'get_named_op_par':{
		'parameters':{
			'name':{
				'type':str
			},
			'par':{
				'type':str
			}
		},
		'required':['name', 'par']
	},
	'put_named_op_attribute':{
		'parameters':{
			'name':{
				'type':str
			},
			'attribute':{
				'type':str
			},
			'value':{
				'type':str
			}
		},
		'required':['name', 'attribute', 'value']
	}
}
def formatMissingParamMessage(param):
	data = {
		'error': {
			'message': f'KeyError: Missing required parameter {param}.'
		}
	}
	
	return (400, 'Bad Request', data)
def formatTypeErrorMessage(param, _type):
	data = {
		'error': {
			'message': f'TypeError: "{param}" must be type {_type}'
		}
	}
	# self.formatResponse(400, 'Bad Request', data)
	return (400, 'Bad Request', data)

def validateParameters(required_pars:list, included_pars:list):
	hasRequired = True

	for p in required_pars:
			# if the parameter name is a string, just check if it's in the included pars
		if type(p) == str and hasRequired:
			hasRequired = hasRequired and (p in included_pars)
		elif type(p) == list:
			# if it's a list, that means that one of the options is required
			# check if any of the options is included in the included pars
			hasTupleOption = any(_p in included_pars for _p in p)
			hasRequired = hasRequired and hasTupleOption


	return hasRequired

def validateTypes(pars, expected_pars):
	validType = True
	for par, val in pars.items():
	
		expected_type = expected_pars[par]['type']
		validType = validType and isinstance(val, expected_type)

		if not validType:
			try:
				expected_type(val)
			except:
				pass
	return validType


def validateParametersDict(pars: dict, schema):
	
	included_pars = pars.keys()				# pars passed from the request
	expected_pars = schema['parameters']	# all possible parameters (may be optional)
	required_pars = schema['required']		# parameters that MUST be included

	hasRequired = True
	validType = False

	hasRequired = validateParameters(required_pars, included_pars)

	if hasRequired:
		validType = validateTypes(pars, expected_pars)
		# for par, val in pars.items():
			
		# 	expected_type = expected_pars[par]['type']
		# 	validType = validType and isinstance(val, expected_type)

		# 	if not validType:
		# 		try:
		# 			expected_type(val)
		# 		except:
		# 			pass

	return hasRequired, validType

class TestValidateParams(unittest.TestCase):

	def test_valid_put_app_power(self):
		actual = validateParametersDict({'state':False}, schemas.get('put_app_power'))
		expected = True, True

		self.assertEqual(actual, expected)
	
	# def test_invalid_type_put_app_power(self):
	# 	actual = validateParametersDict({'state':'false'}, schemas.get('put_app_power'))
	# 	expected = False, True
	# 	self.assertEqual(actual, expected)
	
	def test_valid_put_cookrate_int(self):
		actual = validateParametersDict({'rate':60}, schemas.get('put_project_cookRate'))
		expected = True, True
		self.assertEqual(actual, expected)
	def test_valid_put_cookrate_float(self):
		actual = validateParametersDict({'rate':45.0}, schemas.get('put_project_cookRate'))
		expected = True, True
		self.assertEqual(actual, expected)
	def test_invalid_put_cookrate_str(self):
		actual = validateParametersDict({'rate':'true'}, schemas.get('put_project_cookRate'))
		testMessage = formatTypeErrorMessage('current_param', float.__name__)
		expected = True, False
		self.assertEqual(actual, expected)
	def test_invalid_put_cookrate_wrong_param(self):
		actual = validateParametersDict({'cookrate':60}, schemas.get('put_project_cookRate'))
		testMessage = formatMissingParamMessage('current_param')
		expected = False, False
		self.assertEqual(actual, expected)
	

	def test_valid_put_op_par(self):
		actual = validateParametersDict({'path':'/test', 'par':'test', 'val':'any'}, schemas.get('put_op_par'))
		expected = True, True
		self.assertEqual(actual, expected)

				


if __name__ == '__main__':
	unittest.main()