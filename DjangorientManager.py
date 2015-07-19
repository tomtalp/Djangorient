import json

class DjangorientResultSet(object):
	def __init__(self, resp, content, uri = None):
		self._resp = resp
		self._content = content
		self._uri = uri
		self._check_resp()
		self.results = self._parse_resp_content()

	def _parse_resp_content(self):
		"""
		Parse query results into the results generator
		"""
		resp_dict = self._get_results_dict()

		results = []

		try:
			results_list = resp_dict['result']
		except KeyError:
			return None
		except TypeError: # Raised when results_dict is empty
			return None
	
		for r in results_list:
			values_dict = dict()
			values_dict['id'] = str(r['@rid'])
			values_dict['class_name'] = str(r['@class'])

			for key, val in r.iteritems():
				if not key.startswith('@'):
					values_dict[key] = val

			results.append(type(values_dict['class_name'], (), values_dict))

		return results

	def raw_json_resp(self):
		"""
		JSON formatted representation of the query results
		"""
		return str(self._content)

	def _get_results_dict(self):
		"""
		Query results in a Python dictionary
		"""
		if self._content:
			return json.loads(str(self._content))

	def _check_resp(self):
		if self._resp['status'] == '401':
			raise Exception('Not authorized! Please enter a valid username & pw')
