from bs4 import BeautifulSoup
from urllib.request import urlopen
from constants import *
import logging
import traceback
import ssl


def format_word(word):
    return word.replace(" ", "-")


def get_sound_location(word, language_code="en-US"):
    """Get an audio url of word from the Oxford site"""

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    url = ENGLISH_SRC + format_word(word)
    try:
        f = urlopen(url, context = context)
    except:
        logging.error(traceback.format_exc())
        return ""
    html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    if language_code == "en-US":
        audio_divs = soup.find_all("div", {"class": "sound audio_play_button pron-us icon-audio"})
    else:
        audio_divs = soup.find_all("div", {"class": "sound audio_play_button pron-uk icon-audio"})

    if len(audio_divs) == 0:
        return ""

    else:
        location = audio_divs[0]["data-src-mp3"]
        return location


def get_pronunciation(word, language_code="en-US"):
    url = ENGLISH_SRC + format_word(word)
    try:
        f = urlopen(url)
    except:
        return ""
    html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    if language_code == "en-US":
        ind = 'NAmE'
        pronunciations = soup.find_all("span", {"class": "phon"})
    else:
        ind = 'BrE'
        pronunciations = soup.find_all("div", {"class": "phone"})

    if len(pronunciations):
        for pron in pronunciations:
            if ind in pron.text:
                p = pron.text
                p = p.replace("NAmE", "")
                p = p.replace("//", "")
                return p

    return ""


if __name__ == "__main__":
    pronunciation = get_pronunciation("afsa")
    print(pronunciation)
