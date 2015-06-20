class String(object):
	def __init__(self):
		pass

	def return_orientdb_type(self):
		return "STRING"

class Integer(object):
	def __init__(self):
		pass

	def return_orientdb_type(self):
		return "INTEGER"


global all_types 
all_types = [String, Integer]