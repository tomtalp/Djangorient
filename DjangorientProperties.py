class DjangorientType(object):
	def __init__(self):
		pass

	def validate_type(self, val, try_converting = True):
		if isinstance(val, self.get_python_type()):
			return val
		else:
			if not try_converting:
				raise Exception("Value {val} is expected to be of type {prop_type}".format(val = val, prop_type = self.__name__))
			else:
				try:
					return self.convert_to_type(val)
				except Exception, e:
					raise e


	def get_python_type(self):
		# Will only be raised if inheriting classes don't implement this function
		raise Exception("Python type not implemented....")

	def convert_to_type(self):
		# Will only be raised if inheriting classes don't implement this function
		raise Exception("Conversion function not implemented....")


class String(DjangorientType):
	def __init__(self):
		super(String, self).__init__()

	def get_orientdb_type(self):
		return "STRING"

	def get_python_type(self):
		return str

	def convert_to_type(self, val):
		"""
		Try converting a value to this type
		"""
		try:
			return str(val)
		except ValueError, e:
			raise e	
		
class Integer(DjangorientType):
	def __init__(self):
		super(Integer, self).__init__()

	def get_orientdb_type(self):
		return "INTEGER"

	def get_python_type(self):
		return int

	def convert_to_type(self, val):
		"""
		Try converting a value to this type
		"""
		try:
			return int(val)
		except ValueError, e:
			raise e


global all_types 
all_types = [String, Integer]