from django.conf import settings
from bulbs.rexster import RexsterClient
from bulbs.config import Config
from DjangorientQueryManager import DjangorientQueryManager

class DjangorientConnection(object):
	def __init__(self):

		self.connection = None
		self._rexster_config = None
		self.QueryManager = None

	def _create_bulb_config(self):
		"""
		Build a bulbs Rexster configuration object via settings.py data
		"""
		rexster_graph_uri = settings.DJANGORIENT_SETTINGS['REXSTER_DB_URI']
		bulbs_rexster_config = Config(rexster_graph_uri)

		return bulbs_rexster_config

	def setup(self):
		self._rexster_config = self._create_bulb_config()
		self.connect()

	def connect(self):
		try:
			self._rexster_config = self._create_bulb_config()		
			self.connection = RexsterClient(self._rexster_config)
		except Exception, e:
			raise e

	def close(self):
		pass

	def query_manager(self):
		"""
		Return the query manager object
		"""
		self.QueryManager = DjangorientQueryManager(self.connection)
		return self.QueryManager

	def create_query_manager(self):
		"""
		Initialize the Djangorient QueryManager
		"""
		self.QueryManager = DjangorientQueryManager(self.connection)


	def test_query(self):
		"""
		TEST
		"""
		print self.connection.gremlin("g.V.count()").results.next().data


c = DjangorientConnection()
c.connect()
qm = c.query_manager()
results = qm.gremlin("g.V.count()")
print results.results_iter.next().data