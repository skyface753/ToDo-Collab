from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os

CASSANDRA_PASSWORD = os.environ.get('CASSANDRA_PASSWORD', 'cassandra')
CASSANDRA_USERNAME = os.environ.get('CASSANDRA_USERNAME', 'cassandra')
CASSANDRA_HOST = os.environ.get('CASSANDRA_HOST', '127.0.0.1')

auth_provider = PlainTextAuthProvider(
    username=CASSANDRA_USERNAME, password=CASSANDRA_PASSWORD)
cluster = Cluster([CASSANDRA_HOST], auth_provider=auth_provider)

session = cluster.connect()
KEYSPACE = 'test'


def clear_keyspace():
    session.execute('DROP KEYSPACE IF EXISTS %s' % KEYSPACE)


session.execute("""
    CREATE KEYSPACE IF NOT EXISTS %s
    WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
    """ % KEYSPACE)

session.set_keyspace(KEYSPACE)

# Call clear_keyspace if main
if __name__ == '__main__':
    clear_keyspace()
