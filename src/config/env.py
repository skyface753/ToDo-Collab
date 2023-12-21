import os

AUTH_SECRET = os.environ.get('AUTH_SECRET', 'secret')
USE_WSS = False
USE_WSS_STR = os.environ.get('USE_WSS', 'false')
if USE_WSS_STR.lower() == 'true' or USE_WSS_STR.lower() == '1':
    USE_WSS = True
