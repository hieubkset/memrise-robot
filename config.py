# To find the TEXT_TO_SPEECH_SRC
# go to the https://soundoftext.com/
# make a mock download
# press F12
# go to network tab
# see headers --> request url
TEXT_TO_SPEECH_SRC = 'https://api.soundoftext.com/sounds'
SOUNDS_POST_CMD = '{{"engine": "Google", "data": {{"text": "{0}", "voice": "{1}"}}}}'
#
import os
cwd = os.getcwd()
RELATIVE_TEMP_FILE_PATH = "audio/temp.mp3"
TEMP_FILE_PATH = os.path.join(cwd, RELATIVE_TEMP_FILE_PATH)
#
ENGLISH_SRC = 'https://www.oxfordlearnersdictionaries.com/definition/english/'
MEMRISE_HOMEPAGE_URL = "https://community-courses.memrise.com/"
USERNAME = 'memrise.robot'
PASSWORD = '123456'
DELAY_TIME = 1.5
PRONUNCIATION = False
NUM_RETRY = 3