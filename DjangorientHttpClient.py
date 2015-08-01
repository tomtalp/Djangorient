import httplib2
import base64
import json
from djangorient.DjangorientResultsManager import *

class HttpClient(object):
	def __init__(self, base_uri, db_name, username, password):
		print "Created HTTP Client!"
		self._http = httplib2.Http()

		self._username = username
		self._password = password
		self._base64_auth = self._get_base64_auth()

		self._request_headers = self._get_headers()
		self._base_uri = base_uri
		self._db_name = db_name

	def _get_base64_auth(self):
		"""
		Return the authentication credentials in a base64 format
		"""
		return base64.encodestring(self._username + ':' + self._password)

	def _get_headers(self):
		"""
		Headers for HTTP request
		"""
		return {'Content-Type': 'application/json; charset=UTF-8',
				'Accept-Encoding': 'gzip,deflate',
				'Authorization': 'Basic ' + self._base64_auth}

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
		return DjangorientResultSet(resp, content, uri)

	def _GET_request(self, uri):
		resp, content = self._http.request(
			uri = uri,
			method = 'GET',
			headers = self._request_headers,
		)

		return DjangorientResultSet(resp, content, uri)

