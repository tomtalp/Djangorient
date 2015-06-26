from djangorient.Djangorient import *
from djangorient.DjangorientProperties import *

class DjangorientModel(object):
	def test_conn(selft):
		return client
		

class DjangorientNode(DjangorientModel):
	def __init__(self):
		super(DjangorientNode, self).__init__()

	def all(self):
		pass

	def raw_sql(self, user_query):
		results = client.run_sql_query(user_query)
		return results
		print results

	def create(self, **kwargs):
		return self


class DjangorientBuilder(object):
	"""
	A utility for building schemas in the database, based on the user
	defined models in models.py
	"""

	def __init__(self):
		self.user_classes = dict()

	def build_classes_dict(self):
		subclasses = DjangorientNode.__subclasses__()
		
		for cls in subclasses:
			class_name = cls.__name__
			self.user_classes[class_name] = dict()
			for attr in dir(cls):
				obj_property = getattr(cls, attr)

				# Test if the property is of a recognized type
				if filter(lambda x: x is type(obj_property), all_types):
					self.user_classes[class_name][attr] = obj_property.return_orientdb_type()

	def write_classes(self):
		"""
		Write the user-defined classes to the DB.
		"""
		for class_name, class_properties in self.user_classes.iteritems():
			client.create_class(class_name, class_properties)


# d1 = DjangorientBuilder()
# d1.build_classes_dict()
# d1.write_classes()
#client._http_client.create_class()