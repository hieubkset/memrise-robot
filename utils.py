import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import platform
from config import MEMRISE_HOMEPAGE_URL, USERNAME, PASSWORD, DELAY_TIME, NUM_RETRY, TEMP_FILE_PATH
import time
import logging


def get_url(browser, url):
    browser.get(url)
    time.sleep(DELAY_TIME)


def is_auto_driver_support():
    selenium_version = selenium.__version__
    version_numbers = tuple(map(int, selenium_version.split('.')))
    target_version = (4, 6, 0)
    return version_numbers > target_version


def create_browser():
    if is_auto_driver_support():
        browser = webdriver.Chrome()
    else:
        if platform.system() == 'Darwin':
            browser = webdriver.Chrome("./chrome/macos/chromedriver")
        elif platform.system() == 'Windows':
            browser = webdriver.Chrome("./chrome/windows/chromedriver")
        else:
            browser = webdriver.Chrome("./chrome/linux/chromedriver")
    return browser


def find_element_with_retry(browser, method, value):
    element = None
    count = 0
    while count < NUM_RETRY:
        try:
            element = browser.find_element(method, value)
            return element
        except NoSuchElementException:
            time.sleep(DELAY_TIME)
            count += 1


def click_login(browser, login_button):
    browser.execute_script("arguments[0].click();", login_button)
    time.sleep(DELAY_TIME)


def login_memrise():
    """Login into memrise robot account"""

    browser = create_browser()
    get_url(browser, MEMRISE_HOMEPAGE_URL)

    username_textfield = find_element_with_retry(browser, By.ID, "username")
    if username_textfield is None:
        logging.info('Can not find the username field.')
        return None

    pass_textfield = find_element_with_retry(browser, By.ID, "password")
    if pass_textfield is None:
        logging.info('Can not find the password field.')
        return None

    login_button = find_element_with_retry(
        browser, By.CSS_SELECTOR, "button[type='submit']")
    if login_button is None:
        logging.info('Can not find the loggin button.')
        return None

    pass_textfield.send_keys(PASSWORD)
    username_textfield.send_keys(USERNAME)
    click_login(browser, login_button)

    return browser


def is_contributor(browser, memrise_course):
    """Check if memrise robot account was given the contribution permission"""

    get_url(browser, memrise_course)

    if 'database' in browser.current_url:
        return True
    else:
        return False


def find_number_of_page(browser):
    """Find the number of page in the database page"""
    try:
        page_number_container = browser.find_element(
            By.CSS_SELECTOR, "div.pagination.pagination-centered > ul")
    except NoSuchElementException:
        return -1
    else:
        page_number_elements = page_number_container.find_elements(
            By.CSS_SELECTOR, "li")

        if len(page_number_elements) > 1:
            last_page_number_element = page_number_elements[-2]
            return int(last_page_number_element.text)
        else:
            return 1


def has_audio(row):
    text_cells = row.find_elements(By.CLASS_NAME, "cell")
    text_in_file = text_cells[2].find_element(By.CLASS_NAME, "dropdown-toggle").text
    return any(char.isdigit() for char in text_in_file)


def get_rows_of_word(browser):
    rows_of_word = browser.find_elements(By.CLASS_NAME, "thing")
    return rows_of_word


def get_word(row):
    text_cells = row.find_elements(By.CLASS_NAME, "cell")
    word = text_cells[0].text
    word = word.lower()
    return word


def upload_audio(row):
    text_cells = row.find_elements(By.CLASS_NAME, "cell")
    upload_button = text_cells[2].find_elemente(By.CLASS_NAME, "add_thing_file")
    upload_button.send_keys(TEMP_FILE_PATH)