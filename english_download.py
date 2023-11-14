from bs4 import BeautifulSoup
from config import *
import requests


def format_word(word):
    return word.replace(" ", "-")


def get_sound_location(word, language_code="en-US"):
    """Get an audio url of word from the Oxford site"""
    headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    url = ENGLISH_SRC + format_word(word)
    response = requests.get(url, headers=headers)
    html = response.text
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
    headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    if language_code == "en-US":
        ind = 'NAmE'
        pronunciation_div = soup.find("div", class_="phons_n_am")
    else:
        ind = 'BrE'
        pronunciation_div = soup.find("div", class_="phons_br")

    pronunciation  = pronunciation_div.find('span').text

    return pronunciation


if __name__ == "__main__":
    pronunciation = get_sound_location("numerous")
    print(pronunciation)
