import httplib2
import json

class HttpClient(object):
	def __init__(self, base_uri, db_name, username, password):
		print "Created HTTP Client!"
		self._http = httplib2.Http()
		self._http.add_credentials(username, password)
		self._request_headers = self._get_headers()

		self._base_uri = base_uri
		self._db_name = db_name

	def _get_headers(self):
		"""
		Headers for HTTP request
		"""
		return {'Content-Type': 'application/json; charset=UTF-8',
				'Accept-Encoding': 'gzip,deflate'}

	def send_request(self, uri, method, data=None):
		if type(data) is str:
			try:
				json.loads(data)
			except ValueError, e:
				raise Exception("The JSON format of your data is invalid")

		elif type(data) is dict:
			data = json.dumps(data)

		elif data is not None:
			raise Exception("Data must a dictionary or raw JSON")

		## TODO - Add more methods
		if method.upper() == 'POST':
			return self._POST_request(uri, data)
		else:
			return self._GET_request(uri)

	def _POST_request(self, uri, data = None):
		headers = self._request_headers
		# if data:
		# 	headers['Content-Length'] = str(len(data))

		resp, content = self._http.request(
			uri = uri,
			method = 'POST',
			headers = headers,
			body = data
		)
		return DjangorientResults(resp, content, uri)

	def _GET_request(self, uri):
		resp, content = self._http.request(
			uri = uri,
			method = 'GET',
			headers = self._request_headers,
		)

		return DjangorientResults(resp, content, uri)

class DjangorientResults(object):
	def __init__(self, resp, content, uri = None):
		self._resp = resp
		self._content = content
		self._uri = uri
		self._check_resp()

	def __str__(self):
		return self._content

	def _check_resp(self):
		if self._resp['status'] == '401':
			raise Exception('Not authorized! Please enter a valid username & pw')

