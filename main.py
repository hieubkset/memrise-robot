from utils import login_memrise, is_contributor, find_number_of_page, has_audio, get_url, get_rows_of_word, get_word, upload_audio
from audio_download import create_audio_file
from english_download import get_pronunciation
from config import *
import logging
import logging

logging.basicConfig(
    format='[%(asctime)s - %(name)s - %(levelname)s] %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def memrise_page_upload(browser, memrise_page, language_code="en-US"):
    """Download audio files for a memrise page"""
    get_url(browser, memrise_page)

    rows_of_word = get_rows_of_word(browser)

    for row in rows_of_word:
        word = get_word(row)
 
        if not has_audio(row):
            if create_audio_file(word, language_code):
                upload_audio()
                logger.info('Upload an audio file for ' + word)
            else:
                logger.error("Failed for word: %s" % word)


def memrise_upload(url, start_page=1, language_code="en-US"):
    """Download audio files for a memrise course"""

    browser = login_memrise()
    if browser is None:
        logger.info('Login failed!')
    else:
        logger.info('Login successfully!')
        if not is_contributor(browser, url):
            logger.info(
                'Please add "memrise.robot" as a contributor of your course!')
        else:
            logger.info('Memrise.robot is a contributor')

            number_of_page = find_number_of_page(browser)
            logger.info('The number of page is ' + str(number_of_page))

            if number_of_page == -1:
                memrise_page_upload(browser, url, language_code)
            else:
                for i in (start_page, number_of_page + 1):
                    page_url = url + "?page=" + str(i)
                    memrise_page_upload(browser, page_url, language_code)


if __name__ == "__main__":
    start_page = 1
    url = "https://app.memrise.com/course/6235501/pmp/edit/database/7281972/"
    language_code = 'en-US'
    memrise_upload(url, start_page, language_code)
