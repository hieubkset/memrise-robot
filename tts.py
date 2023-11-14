from config import *
import requests
import json
from json.decoder import JSONDecodeError


def get_sound_id(word, language_code):
    """Request server to create a tts sound from word and language code and return it's id"""

    headers = {"Content-type": "application/json"}
    data = SOUNDS_POST_CMD.format(word, language_code)
    data = data.encode("utf-8")

    response = requests.post(TEXT_TO_SPEECH_SRC, headers=headers, data=data)
    try:
        json_response_content = json.loads(response.content)
    except JSONDecodeError:
        _id = ""
    else:
        _id = json_response_content["id"]

    return _id


def get_sound_url_by_id(_id):
    """Get location of a created audio from it's id"""

    url = TEXT_TO_SPEECH_SRC + "/" + _id

    response = requests.get(url)
    json_response_content = json.loads(response.content)
    location = json_response_content["location"]
    return location


def get_sound_url(word, language_code):
    """Get location of an word from any country"""

    _id = get_sound_id(word, language_code)
    if len(_id) == 0:
        return ""
    else:
        try:
            location = get_sound_url_by_id(_id)
        except KeyError:
            location = get_sound_url_by_id(_id)
        return location
