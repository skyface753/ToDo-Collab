from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os

CASSANDRA_PASSWORD = os.environ.get('CASSANDRA_PASSWORD', 'cassandra')


auth_provider = PlainTextAuthProvider(
    username='cassandra', password=CASSANDRA_PASSWORD)
cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)

session = cluster.connect()
KEYSPACE = 'test'

# Clear keyspace
session.execute('DROP KEYSPACE IF EXISTS %s' % KEYSPACE)


session.execute("""
    CREATE KEYSPACE IF NOT EXISTS %s
    WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
    """ % KEYSPACE)

session.set_keyspace(KEYSPACE)
