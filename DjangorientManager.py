from djangorient.Djangorient import *
from djangorient.DjangorientProperties import all_types

class DjangorientBaseManager(object):
	"""
	Base class for an Edge/Node 'objects' manager
	"""
	def __init__(self, cls):
		self._cls = cls
		self._class_name = self._cls.__name__

	def all(self):
		"""
		Return all class documents
		"""
		return client.get_all(self._class_name)

	def filter(self, **kwargs):
		"""
		Get documents of a class that match the filters.
		"""
		class_properties = self._get_properties()
		filter_items = dict()

		for key, val in kwargs.iteritems():
			# TODO - In the future we'll add filters that aren't a part of
			# the class properties.
			# I.E - greater_than/lesser_than properties, between dates etc
			if key not in class_properties and key != 'id':
				raise Exception("The property {property} is not a part of the class {cls}".format(property = key, cls = self._class_name))
			else:
				if key == 'id':
					key = '@rid'
				filter_items[key] = val

		return client.filter_func(self._class_name, filter_items)
		
	def get_by_id(self, id):
		"""
		Get a class by an id (ID has to match OrientDB ID format, I.E - '#12:2')
		"""
		r = self.filter(id = id)
		if r.results: 
			return r[0]

	def _get_properties(self):
		"""
		Return all the properties defined by the user in the class
		(Will be used by subclasses that inherit DjangorientNode)
		"""
		properties = dict()
		cls = self._cls

		for key, val in cls.__dict__.iteritems():
			if filter(lambda x: x is type(val), all_types):
				properties[key] = val
		return properties

	def _get_property_value(self, property_value, property_type):
		"""
		Validate the property value with its selected type, and try to convert if incompatible
		"""
		try:
			val = property_type.validate_type(property_value, try_converting = True)
		except Exception, e:
			raise e

		return val

class DjangorientNodeManager(DjangorientBaseManager):
	"""
	Manager for OrientDB Nodes (vertices)
	"""

	def __init__(self, cls):
		super(DjangorientNodeManager, self).__init__(cls)

	def create(self, **kwargs):
		"""
		Create a document in the database, based on a certain class.
		"""
		class_properties = self._get_properties()
		property_values = dict()

		for key, val in kwargs.iteritems():
			if key not in class_properties:
				raise Exception("The property {property} is not a part of the class {cls}".format(property = key, cls = self._class_name))
			else:
				property_values[key] = self._get_property_value(val, class_properties[key])

		return client.add_to_class(self._class_name, property_values)

class DjangorientEdgeManager(DjangorientBaseManager):
	"""
	Manager for OrientDB Edges
	"""

	def __init__(self, cls):
		super(DjangorientEdgeManager, self).__init__(cls)

	def create(self, in_node, out_node, **kwargs):
		"""
		Create an edge from the incoming node to the outcoming node
		"""

		class_properties = self._get_properties()
		property_values = dict()

		for node in [in_node, out_node]:
			if not self._validate_node(node):
				raise Exception("{n} cannot be connected by edges...".format(n = str(node)))

		for key, val in kwargs.iteritems():
			if key not in class_properties:
				raise Exception("The property {property} is not a part of the class {cls}".format(property = key, cls = self._class_name))
			else:
				property_values[key] = self._get_property_value(val, class_properties[key])

		return client.add_edge(self._class_name, in_node.id, out_node.id, property_values)


	def _validate_node(self, node):
		"""
		Validate whether the node has vertex attributes & can be connected via an edge
		"""
		return hasattr(node, 'id') and hasattr(node, 'class_name')

		
