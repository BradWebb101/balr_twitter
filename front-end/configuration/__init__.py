from app import app
import urllib
import os

# secret key for user session
app.secret_key = "ITSASECRET"

#database connection parameters
connection_params = {
    'user': '',
    'password': '',
    'host': '',
    'port': 'port',
    'namespace': '',
}
