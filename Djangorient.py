from django.conf import settings
from djangorient.DjangorientHttpClient import HttpClient
import json
import urllib


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
							self._db_name,
							self._username, 
							self._password)

	def disconnect(self):
		"""
		Send a GET request to the disconnect URI 
		(kills the session?)
		"""
		disconn_uri = self._base_uri + '/disconnect/'
		self._http_client.send_request(disconn_uri, 'GET')

	
	def create_base_class(self, class_name, class_properties):
		"""
		Creates a base class
		"""
		uri = '{base}/class/{db_name}/{class_name}/'.format(
														base = self._base_uri,
														db_name = self._db_name,
														class_name = class_name)
		
		self._http_client.send_request(uri, 'POST')

		self.add_properties_to_class(class_name, class_properties)


	def create_class(self, class_name, class_properties):
		"""
		Creates a class which extends from V or E, via an SQL query 
		"""	
		superclass = class_properties.pop('superClass')
		creation_query = 'CREATE CLASS {cls_name} EXTENDS {superclass}'.format(cls_name = class_name, superclass = superclass)
		self.exec_sql_query(creation_query, 'POST')

		self.add_properties_to_class(class_name, class_properties)

	def add_properties_to_class(self, class_name, class_properties):
		"""
		Add properties to a given class
		"""
		uri = '{base}/property/{db_name}/{class_name}/'.format(
														base = self._base_uri,
														db_name = self._db_name,
														class_name = class_name)

		data = dict()

		for prop_name, prop_type in class_properties.iteritems():
			data[prop_name] = {"propertyType": prop_type}

		self._http_client.send_request(uri, 'POST', data)

	def exec_gremlin_query(self, query, method):
		"""
		Execute Gremlin queries via the command service
		"""
		urlencoded_query = urllib.quote(query)
		uri = '{base}/command/{db_name}/gremlin/{query}'.format(
														base = self._base_uri,
														db_name = self._db_name,
														query = urlencoded_query)

		results = self._http_client.send_request(uri, method)
		return results


	def exec_sql_query(self, query, method = 'GET'):
		"""
		Execute a SQL query via the command service.
		Using 'command' instead of query because we need idempotent queries support.
		"""
		#no_whitespace_query = query.replace(' ', '%20')
		urlencoded_query = urllib.quote(query)
		uri = '{base}/command/{db_name}/sql/{query}'.format(
														base = self._base_uri,
														db_name = self._db_name,
														query = urlencoded_query)

		results = self._http_client.send_request(uri, method)
		return results

	def add_to_class(self, class_name, values):
		"""
		Add a document (node or edge) to a class
		"""
		json_values = json.dumps(values)
		insertion_sql_query = "INSERT INTO {class_name} content {json_content}".format(class_name = class_name, json_content = json_values)
		return self.exec_sql_query(insertion_sql_query, method = 'POST')

	def add_edge(self, edge_name, in_id, out_id, values):
		"""
		Create an Edge from the incoming id to the outcoming id
		"""
		json_values = json.dumps(values)
		creation_sql_query = "CREATE EDGE {edge_name} FROM {in_id} TO {out_id} CONTENT {json_content}".format(edge_name = edge_name, in_id = in_id, out_id = out_id, json_content = json_values)
		return self.exec_sql_query(creation_sql_query, method = 'POST')		

	def get_all(self, class_name):
		"""
		Run a SELECT * query to get all documents of a class
		"""
		return self.exec_sql_query(
				"SELECT * FROM {class_name}".format(class_name = class_name),
				method = "POST")

	def filter_func(self, class_name, filter_items):
		"""
		Run a query to get all documents of a class, with the applied filters.
		"""
		base_query = "SELECT * FROM {cls_name} WHERE {filters}"

		filters_list = []

		for key, val in filter_items.iteritems():
			filters_list.append("{key} = '{val}'".format(key = key, val = val))

		filters_str = " AND ".join(filters_list)

		final_query = base_query.format(cls_name = class_name, filters = filters_str)

		return self.exec_sql_query(final_query)

	## TODO - Implement a proper test
	def test_connection(self):
		conn_uri = self._base_uri + '/connect/' + self._db_name
		return self._http_client.send_request(conn_uri, 'GET')

	def test_GET(self):
		uri = self._base_uri + '/document/' + self._db_name + '/1:0'
		r1 = self._http_client.send_request(uri, 'GET')
		return r1

	
client = DjangorientClient()
#client.test_connection()
