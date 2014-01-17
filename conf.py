import os

class Config(object):
    DEBUG = True
    TESTING = False
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
    FBAPI_APP_ID = os.environ.get('FACEBOOK_APP_ID')
    FBAPI_APP_SECRET = os.environ.get('FACEBOOK_SECRET')
    FBAPI_SCOPE = ['user_likes', 'user_photos', 'user_photo_video_tags']
    SECRET_KEY = "d5X2=!T774/=$z#(c@K3"

    if(DEBUG):
        DATABASE_URL = "postgres://postgres:DBDAdmin2005@localhost:5432/blink_local"
    else:
        DATABASE_URL = os.environ.get('DATABASE_URL')

    #DATABASE_URL = 'postgres://vfmjwyuzoqtsif:TAnQ-sge91VHtSePg4uPvole35@ec2-23-21-130-189.compute-1.amazonaws.com:5432/dd660iq7u04p1b'