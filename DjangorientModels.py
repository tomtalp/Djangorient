from djangorient.Djangorient import *
from djangorient.DjangorientProperties import *
from djangorient.DjangorientManager import *


class DjangorientBaseNode(type):
	"""
	Metaclass for Nodes & Edges
	"""
	def __new__(cls, name, bases, attrs):
		#super(DjangorientBaseModel, cls).__new__(name, bases, attrs)
		super_new = super(DjangorientBaseNode, cls).__new__

		# DjangorientNode/Edge don't require any additional attributes, so return them with no additions
		if name in ['DjangorientNode', 'DjangorientEdge']:
			return super_new(cls, name, bases, attrs)
		
		new_cls = super_new(cls, name, bases, attrs)
		setattr(new_cls, 'objects', DjangorientNodeManager(new_cls))
		
		return new_cls
		
class DjangorientNode(object):
	__metaclass__ = DjangorientBaseNode

	def __init__(self):
		#super(DjangorientNode, self).__init__()
		self._class_name = self.__class__.__name__

	@classmethod
	def _get_superclass(cls):
		return 'V'

class DjangorientBaseEdge(type):
	"""
	Metaclass for Nodes & Edges
	"""
	def __new__(cls, name, bases, attrs):
		#super(DjangorientBaseModel, cls).__new__(name, bases, attrs)
		super_new = super(DjangorientBaseEdge, cls).__new__

		# DjangorientNode/Edge don't require any additional attributes, so return them with no additions
		if name in ['DjangorientNode', 'DjangorientEdge']:
			return super_new(cls, name, bases, attrs)
		
		new_cls = super_new(cls, name, bases, attrs)
		setattr(new_cls, 'objects', DjangorientEdgeManager(new_cls))
		
		return new_cls

class DjangorientEdge(object):
	__metaclass__ = DjangorientBaseEdge

	def __init__(self):
		#super(DjangorientNode, self).__init__()
		self._class_name = self.__class__.__name__

	@classmethod
	def _get_superclass(cls):
		return 'E'

class DjangorientBuilder(object):
	"""
	A utility for building schemas in the database, based on the user
	defined models in models.py
	"""

	def __init__(self):
		self.user_classes = dict()
		self.build_classes_dict()
		self.write_classes()

	def build_classes_dict(self):
		subclasses = DjangorientNode.__subclasses__()
		subclasses += DjangorientEdge.__subclasses__()
		
		for cls in subclasses:
			class_name = cls.__name__
			self.user_classes[class_name] = dict()
			self.user_classes[class_name]['superClass'] = cls._get_superclass()
			for attr in dir(cls):
				obj_property = getattr(cls, attr)

				# Test if the property is of a recognized type
				if filter(lambda x: x is type(obj_property), all_types):
					self.user_classes[class_name][attr] = obj_property.get_orientdb_type()


	def write_classes(self):
		"""
		Write the user-defined classes to the DB.
		"""
		for class_name, class_properties in self.user_classes.iteritems():
			client.create_class(class_name, class_properties)
