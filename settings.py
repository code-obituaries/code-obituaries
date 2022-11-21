import json
import os  

OUTPUT_FOLDER = 'docs/'
PROFILE_FOLDER = os.path.join(OUTPUT_FOLDER, 'profile')
DATA_FOLDER = './data'
info = None

with open('info.json') as f:
    info = json.load(f)
