from django.conf import settings
from djangorient.DjangorientHttpClient import HttpClient

class DjangorientClient(object):
	def __init__(self):
		self._username = settings.DJANGORIENT_SETTINGS['username']
		self._password = settings.DJANGORIENT_SETTINGS['password']
		self._db_name = settings.DJANGORIENT_SETTINGS['name']
		self._host = settings.DJANGORIENT_SETTINGS['host']
		self._port = settings.DJANGORIENT_SETTINGS['port']
		self._base_uri = 'http://{host}:{port}'.format(host = self._host, port = self._port)
		self._http_client = HttpClient(
							self._base_uri, 
							self._db_name
							self._username, 
							self._password)

	def disconnect(self):
		disconn_uri = self._base_uri + '/disconnect/'
		self._http_client.send_request(disconn_uri, 'GET')

	## TODO - Implement a proper test
	def test_connection(self):
		conn_uri = self._base_uri + '/connect/' + self._db_name
		return self._http_client.send_request(conn_uri, 'GET')

	def test_GET(self):
		uri = self._base_uri + '/document/' + self._db_name + '/1:0'
		r1 = self._http_client.send_request(uri, 'GET')
		return r1


	
c1 = DjangorientClient()
c1.test_connection()
#print c1.test_GET()


#h1 = c1._http_client
