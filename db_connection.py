import os
import psycopg2
import urlparse

DATABASE_URL = 'postgres://nurpkzhfspjxpx:xdQNuEeCnGu0siyeSEvUGEU7fp@ec2-54-225-255-208.compute-1.amazonaws.com:5432/d9ivq0hggrk4ip'
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ[DATABASE_URL])

def ConnectToDB():
	return psycopg2.connect(database=url.path[1:],
						    user=url.username,
						    password=url.password,
						    host=url.hostname,
						    port=url.port)

def GetCursorForConnection(connection):
	return connection.cursor()
