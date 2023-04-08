import json

def HandleGET(request, response):
	
	uri_split = request["uri_split"]
	
	if uri_split[1] == "op":
		# get operator name, attribute to get (may be member or par)
		# and path to getter module
		op_name, attrib, path = parseOpURI(uri_split)

		# append /get
		path += "/get"

		# look up the operator's path in named_ops dictionary
		try:
			op_path = me.parent().storage["named_operators"][op_name]
			
		except KeyError:
			data = {
				"uri":request["uri"],
				"error":f'{op_name} is not a Named Operator.'
			}
			formatResponse(response, 404, "Not Found", data)
		else:
				# use getter module to get value
			data = mod(path).get([op_path, attrib])

			data = {
				"request":request["uri"],
				"data":data
			}
			formatResponse(response, 200, "OK", data)

		# response['statusCode'] = 200
		# response['statusReason'] = "OK"
		# response['data'] = data
	
	else:
		path = "/".join(uri_split)
		path += "/get"

		try:
			data = mod(path).get()
			data = {
				"data":data,
				"links":{
					"self":request["uri"]
				}
			}

			formatResponse(response, 200, "OK", data)

		except Exception as e:
			if type(e) == tdError:
				# most likely error, resulting from `module not found`
				data = {
					"error":"tdError",
					"links":{
						"self":request["uri"]
					}
				}
				formatResponse(response, 404, "Not Found", data)
			else:
				# some other unknown error
				data = {
					
					"error":"unknown",
					"links":{
						"self":request["uri"]
					}
					
				}
				formatResponse(response, 400, "Bad Request", data)

	return response

def HandlePOST(request, response):
	
	uri_split = request["uri_split"]

	if uri_split[1] == "op":
		op_name, attrib, path = parseOpURI(uri_split)
		value = json.loads(request["data"])["value"]

		path += "/post"
		op_path = op.iTRAP.storage["named_operators"][op_name]
		data = mod(path).post([op_path, attrib, value])

		if data == "success":
			data = json.dumps({
				"uri":request["uri"],
				"success":data
			})
			response['statusCode'] = 200
			response['statusReason'] = "OK"
			response['data'] = data
		elif data == -1:
			data = json.dumps({
				"uri":request["uri"],
				"error":f'{attrib} is not an attribute of {op_name}'
			})
			response['statusCode'] = 400
			response['statusReason'] = "Bad Request"
			response['data'] = data
	
	else:
		path = "/".join(uri_split)
		path += "/post"

		try:
			params = json.loads(request["data"])
			data = mod(path).post(params)
			data = {
				"result":"success",
				"links":{
					"self":request["uri"]
				}
			}
			formatResponse(response, 200, "OK", data)
		except Exception as e:
			print(e)

def HandlePUT():
	pass

def HandlePATCH():
	pass

def parseOpURI(uri):
	# extract name and attribute (or par) from uri
	op_name = uri[2]
	attrib = uri[-1]

	# strip op_name and attrib from uri and join back into path
	uri = uri[:2] + uri[3:-1]
	uri = "/".join(uri)

	return [op_name,attrib,uri]

def formatResponse(response, code, reason, data):
	response["statusCode"] = code
	response["statusReason"] = reason
	response["data"] = json.dumps(data)

	# no reason to return, because we are passing the response dict