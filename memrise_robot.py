from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from audio_download import create_audio_file
from english_download import get_pronunciation
from constants import *
import logging
import traceback
import re


def memrise_login():
    """Login into memrise robot account"""

    browser = webdriver.Chrome("./chrome/linux/chromedriver")
    browser.get(MEMRISE_HOME)

    # login_button = browser.find_element_by_css_selector("#header > div > ul > li:nth-child(2) > a")
    # login_button.click()
    # time.sleep(DELAY_TIME)

    username_textfield = browser.find_element_by_css_selector("#login > div:nth-child(7) > input")
    username_textfield.send_keys(USERNAME)

    pass_textfield = browser.find_element_by_css_selector("#login > div:nth-child(8) > input")
    pass_textfield.send_keys(PASSWORD)

    login_button = browser.find_element_by_css_selector("#login > input.btn-success.btn-large")
    browser.execute_script("arguments[0].click();", login_button)
    # login_button.click()
    time.sleep(DELAY_TIME)

    return browser


def is_contributor(browser, memrise_course):
    """Check if memrise robot account was given the contribution permission"""

    browser.get(memrise_course)

    try:
        browser.find_element_by_css_selector("#page-head > div > div > div > div.course-details > div.course-enroll")
    except NoSuchElementException:
        return True
    else:
        return False


def find_number_of_page(browser):
    """Find the number of page in the database page"""

    try:
        li_container = browser.find_element_by_css_selector("div.pagination.pagination-centered > ul")
    except NoSuchElementException:
        return -1
    else:
        lis = li_container.find_elements_by_css_selector("li")

        if len(lis) == 1:
            return 1
        else:
            last = lis[-2]
            return int(last.text)


def has_audio(thing):
    text_cells = thing.find_elements_by_class_name("cell")
    text_in_file = text_cells[2].find_element_by_class_name("dropdown-toggle").text
    return any(char.isdigit() for char in text_in_file)


def format_word(word):
    """Remove comment out of text"""

    word = re.sub("\(.*\)", "", word)
    word = re.sub("\s+", " ", word)

    return word.strip()


def memrise_page_upload(browser, memrise_page, language_code="en-US", format=False):
    """Download audio files for a memrise page"""
    browser.get(memrise_page)
    time.sleep(DELAY_TIME)
    things = browser.find_elements_by_class_name("thing")

    for thing in things:
        text_cells = thing.find_elements_by_class_name("cell")
        word = text_cells[0].text
        word = word.lower()
        if not has_audio(thing):
            if format:
                word = format_word(word)

            if create_audio_file(word, language_code):
                upload_button = text_cells[2].find_element_by_class_name("add_thing_file")
                upload_button.send_keys(TEMP_FILE_PATH)
            else:
                print("Failed for word: %s" % word)


def memrise_upload(url, skip_page = 1, language_code="en-US"):
    """Download audio files for a memrise course"""

    browser = memrise_login()

    if not is_contributor(browser, url):
        print('Please add "memrise.robot" as a contributor of your course!')
        return False

    number_of_page = find_number_of_page(browser)

    if number_of_page == -1:
        memrise_page_upload(browser, url, language_code)
    else:
        for i in range(skip_page, number_of_page + 1):
            if url[-1] == '/':
                memrise_page_url = url + "?page=" + str(i)
            else:
                memrise_page_url = url + "/?page=" + str(i)

            try:
                memrise_page_upload(browser, memrise_page_url, language_code)
            except Exception:
                logging.error(traceback.format_exc())


if __name__ == "__main__":
    skip_page = 1
    url = "https://www.memrise.com/course/5545461/korean-sogang-1b/edit/database/6565682/"
    language_code = 'ko-KR'
    memrise_upload(url, skip_page, language_code)
    # browser = memrise_login()
    # memrise_page_upload(browser, url, language_code)