import json
from api_routes import api_routes

def putAppPower(request, response):
	power = request["data"]["state"]
	app.power = power

	responseData = {
		'success': True
		}
	response['data'] = json.dumps(responseData)

def getAppPlay(request, response):
	play = request['data']['play']

	return op("/local/time").play

def putAppPlay(request, response):
	play = request['data']['play']
	if type(play) != bool:
		response = formatResponse(response, 400, "Bad Request", {})
		return response
	else:
		op("/local/time").play = play


def getProjectPaths(request, response):
	data = project.paths
	response = formatResponse(response, 200, "OK", data)

def getProjectCookRate(request, response):
	data = project.cookRate
	response = formatResponse(response, 200, "OK", data)

def putProjectCookRate(request, response):
	rate = request['data']['rate']
	rateType = type(rate) == float or type(rate) == (int)
	if not rateType:
		response = formatResponse(response, 400, 'Bad Request', {})
	else:
		project.cookRate = rate
		data = {
			'success':True
		}
		response = formatResponse(response, 200, 'OK', data)

def getProjectRealTime(request, response):
	data = {
		'success':True,
	 	'data':project.realTime
		}
	response = formatResponse(response, 200, 'OK', data)
	

def putProjectRealTime(request, response):
	realTime = request['data']['realTime']
	if type(realTime) != boolean:
		response = formatResponse(response, 400, 'Bad Request', {})
	else:
		project.realTime = realTime
		data = {
			'success':True,
			'data':''
		}
		response = formatResponse(response, 200, 'OK', data)

def getProjectPerformOnStart(request, response):
	performOnStart = project.performOnStart
	data = {
		'success':True,
		'data':performOnStart
	}
	response = formatResponse(response, 200, 'OK', data)

def putProjectPerformOnStart(request, response):
	return

def postProjectLoad(request, response):
	return

def postProjectSave(request, response):
	return

def postProjectQuit(request, response):
	return
def getSysInfoRes(request, response):
	return
def getSysInfoNumMonitors(request, response):
	return
def getUIMasterVolume(request, response):
	return
def putUIMasterVolume(request, response):
	return
def postMonitorsRefresh(request, response):
	return
def getOp(request, response):
	return
def postOp(request, response):
	return
def deleteOp(request, response):
	return
def getOpValid(request, response):
	return
def getOpID(request, response):
	return
def getOpName(request, response):
	return
def putOpName(request, response):
	return
def getOpPath(request, response):
	return
def getOpStorage(request, response):
	return
def getOpTags(request, response):
	return
def postOpTags(request, response):
	return
def deleteOpTags(request, response):
	return
def getOpBypass(request, response):
	return
def putOpBypass(request, response):
	return
def getOpPar(request, response):
	return
def putOpPar(request, response):
	return

def getOpTags(request):
	headers = request['headers']
	path = headers['path']
	return op(path).tags






def HandleRequest(request, response):
	method = request['method']
	uri = request['uri']
	route = f'{method} {uri}'
	data = api_routes[route]

	formatResponse(response, 200, 'OK', data)

	return response

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
			op_path = op.NAPs.OPS(op_name)
			# me.parent().storage["named_operators"][op_name]
			
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

routing_table = {
    "GET /api/v1/app/architecture": app.architecture,
    "GET /api/v1/app/build": app.build,
    "GET /api/v1/app/launchTime": app.launchTime,
    "GET /api/v1/app/osName": app.osName,
    "GET /api/v1/app/power": app.power,
    "PUT /api/v1/app/power": putAppPower,
    "GET/api/v1/app/product": app.product,
    "GET /api/v1/app/version": app.version,
    "GET /api/v1/app/play": getAppPlay,
    "PUT /api/v1/app/play": putAppPlay,

    "GET /api/v1/project/name": project.name,
    "GET /api/v1/project/saveVersion": project.saveVersion,

    "GET /api/v1/project/saveBuild": project.saveBuild,
    "GET /api/v1/project/saveTime": project.saveTime,
    "GET /api/v1/project/saveOSName": project.saveOSName,
    "GET /api/v1/project/saveOSVersion": project.saveOSVersion,
    "GET /api/v1/project/paths": getProjectPaths,
    "GET /api/v1/project/cookRate": getProjectCookRate,
    "PUT /api/v1/project/cookRate": putProjectCookRate,
    "GET /api/v1/project/realTime": getProjectRealTime,
    "PUT /api/v1/project/realTime": putProjectRealTime,
    "GET /api/v1/project/performOnStart": getProjectPerformOnStart,
    "PUT /api/v1/project/performOnStart": putProjectPerformOnStart,
    "POST /api/v1/project/load": postProjectLoad,
    "POST /api/v1/project/save": postProjectSave,
    "POST /api/v1/project/quit": postProjectQuit,

    "GET /api/v1/sysinfo/numCPUs": sysinfo.numCPUs,
    "GET /api/v1/sysinfo/ram": sysinfo.ram,



   
    "GET /api/v1/ui/masterVolume": getUIMasterVolume,
    "PUT /api/v1/ui/masterVolume": putUIMasterVolume,


    "POST /api/v1/monitors/refresh": postMonitorsRefresh,

    "GET /api/v1/op": getOp,
    "POST /api/v1/op": postOp,
    "DELETE /api/v1/op": deleteOp,
    "GET /api/v1/op/valid": getOpValid,
    "GET /api/v1/op/id": getOpID,
    "GET /api/v1/op/name": getOpName,
    "PUT /api/v1/op/name": putOpName,
    "GET /api/v1/op/path": getOpPath,
    "GET /api/v1/op/storage": getOpStorage,
    "GET /api/v1/op/tags": getOpTags,
    "POST /api/v1/op/tags": postOpTags,
    "DELETE /api/v1/op/tags": deleteOpTags,

    "GET /api/v1/op/bypass": getOpBypass,
    "GET /api/v1/op/bypass": putOpBypass,
    "GET /api/v1/op/par": getOpPar,
    "PUT /api/v1/op/par": putOpPar,
}

    # "GET /api/v1/sysinfo/numMonitors": getSysInfoNumMonitors,
    # "GET /api/v1/sysinfo/xres": sysinfo.xres,
    # "GET /api/v1/sysinfo/yres": sysinfo.yres,
    # "GET /api/v1/sysinfo/res": getSysInfoRes,
	    # "GET /api/v1/sysinfo/tfs": sysinfo.tfs,
	# 	    "GET /api/v1/sysinfo/MIDIInputs": sysinfo.MINIInputs,
    # "GET /api/v1/sysinfo/MIDIOutputs": sysinfo.MIDIOuputs,

	#     "GET /api/v1/monitors/height": monitors.height,
    # "GET /api/v1/monitors/numMonitors": monitors.numMonitors,