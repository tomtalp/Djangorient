class DjangorientQueryManager(object):
	def __init__(self, conn):
		self.conn = conn
	
	def gremlin(self, gremlin_script):
		"""
		Execute a Gremlin query against Rexster API & return a results object.
		"""
		bulbs_resp_obj = self.conn.gremlin(gremlin_script)

		return DjangorientResults(bulbs_resp_obj)

class DjangorientResults(object):
	def __init__(self, rexster_response_obj, json_format = False):
		self._rexster_response_obj = rexster_response_obj
		self._raw_http_content = rexster_response_obj.content
		self.results_iter = self.get_results_iter()
		self._json_format = json_format

	def get_results_iter(self):
		return self._rexster_response_obj.results #TEMPORARY IMPLEMENTATION

	def get_all_results(self):
		pass
