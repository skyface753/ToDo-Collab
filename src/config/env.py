import os

AUTH_SECRET = os.environ.get('AUTH_SECRET', 'secret')
USE_WSS = os.environ.get('USE_WSS', False)
