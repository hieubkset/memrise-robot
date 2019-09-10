from tts_download import get_sound_location as tts_location
from english_download import get_sound_location as en_location
from urllib.request import urlretrieve
from constants import *
import traceback
import logging


def create_audio_file(word, language_code):
    """Create an audio file of any word"""

    if language_code == 'en-US' or language_code == 'en-GB':
        location = ""
        try:
            location = en_location(word, language_code)
        except Exception:
            logging.error(traceback.format_exc())
            pass
        # if not location:
        #     print("TTS audio for: %s" % word)
            # location = tts_location(word, language_code)

    # else:
    #     location = tts_location(word, language_code)



    if location:
        urlretrieve(location, TEMP_FILE_PATH)
        return True
    else:
        return False
