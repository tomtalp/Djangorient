import json

# The maximum number of items to display in a ResultSet.__repr__
REPR_OUTPUT_SIZE = 10

class DjangorientResultSet(object):
	def __init__(self, resp, content, uri = None):
		self._resp = resp
		self._content = content
		self._uri = uri
		self._check_resp()
		self.results = self._parse_resp_content()

	def __repr__(self):
		data = [cls for cls in self.results[:REPR_OUTPUT_SIZE + 1]]
		if len(data) > REPR_OUTPUT_SIZE:
			data[-1] = "...(remaining elements truncated)..."
		return repr(data)

	def __getitem__(self, index):
		return self.results[index]

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

			if '@rid' in r:
				values_dict['id'] = str(r['@rid'])
			
			if '@class' in r:
				values_dict['class_name'] = str(r['@class'])

			for key, val in r.iteritems():
				if not key.startswith('@'):
					values_dict[key] = val

			# Only add classes that were queried to the results
			if 'class_name' in values_dict:
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
		try:
			if self._content:
				return json.loads(str(self._content))
		except ValueError, e:
			error_msg = "There seems to be an error... The response we received is - \n" + str(self._content)
			raise Exception(error_msg)
		

	def _check_resp(self):
		if self._resp['status'] == '401':
			raise Exception('Not authorized! Please enter a valid username & pw')
