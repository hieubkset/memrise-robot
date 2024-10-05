from tts import get_sound_url as tts_audio_url
from oxford import get_sound_url as oxford_audio_url
import requests
from config import *
import logging


def create_audio_file(word, language_code):
    """Create an audio file of any word"""

    sound_url = oxford_audio_url(word, language_code)
    if sound_url is None:
        logging.info("TTS audio for: %s" % word)
        sound_url = tts_audio_url(word, language_code)
 
    if sound_url:
        headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
        response = requests.get(sound_url, headers=headers)
        with open(TEMP_FILE_PATH, 'wb') as f:
            f.write(response.content)
        return TEMP_FILE_PATH

    return None
