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
				val = expected_type(val)
				validType = True
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

	return hasRequired, validType