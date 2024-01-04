import unittest
itrap = mod('iTRAP/iTRAP')
class ITRAPTest(unittest.TestCase):
    
	def setUp(self):
		self.banana = itrap.ITRAP(op("iTRAP"))
		self.request = {
			'method': '', 
			'uri': '', 
			'pars': {}, 
			'clientAddress': '127.0.0.1:54284', 
			'serverAddress': '127.0.0.1:29980', 
			'Content-Type': 'application/json', 
			'User-Agent': 'PostmanRuntime/7.32.2', 
			'Accept': '*/*', 
			'Postman-Token': '81291c44-bf75-4d5f-b97a-861ae1e8ee68', 
			'Accept-Encoding': 'gzip, deflate, br', 
			'Connection': 'keep-alive', 
			'Host': 'localhost:29980', 
			'data': b''}
		self.response = {
			'statusCode':200,
			'statusReason':'OK',
			'data':''
		}
	
	def test_get_app_architecture(self):
		self.request["method"] = 'GET'
		self.uri = '/api/banana/app/architecture'
		response = self.banana.HandleRequest(self.request, self.response)
		statusCode = response['statusCode']
		data = response['data']

		self.assertEqual(statusCode, 200)
		self.assertEqual(data, '{"name": "Application Architecture", "scope": "app.architecture", "description": "The architecture of the compile. Generally 32 or 64 bit.", "built-in": true, "data": {"value": 64, "type": "int"}, "links": [{"rel": "self", "href": "http://192.168.50.23:29980/api/banana/app/architecture"}]}')


unittest.main()