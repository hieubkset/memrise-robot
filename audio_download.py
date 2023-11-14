from tts_download import get_sound_location as tts_location
from oxford import get_sound_url
import requests
from config import *
import logging


def create_audio_file(word, language_code):
    """Create an audio file of any word"""

    sound_url = get_sound_url(word, language_code)
    if sound_url is None:
        print("TTS audio for: %s" % word)
        sound_url = tts_location(word, language_code)
 
    if sound_url:
        headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
        response = requests.get(sound_url, headers=headers)
        with open(TEMP_FILE_PATH, 'wb') as f:
            f.write(response.content)
        return TEMP_FILE_PATH

    return None
