import argparse
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pickle
import os


def get_level_urls(url):
    level_urls = []
    f = urlopen(url)
    html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    levels_tag = soup.select_one('div.levels.clearfix')
    levels = levels_tag.select('a.level.clearfix')
    base = 'https://www.memrise.com'
    for level in levels:
        relative = level['href']
        absolute = urljoin(base, relative)
        level_urls.append(absolute)
    return level_urls


def get_level_vocab(url):
    level_name = None
    vocab_bag = {'vocab': [], 'meaning': []}
    f = urlopen(url)
    html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    #
    central_column = soup.select_one('div.central-column')

    # get level name
    tmp = central_column.select_one('div.progress-box.progress-box-level.with-icon')
    tmp = tmp.select_one('h3.progress-box-title')
    level_name = tmp.text
    level_name = level_name.strip()

    # get vocab
    rows = central_column.select('div.thing.text-text')
    for row in rows:
        col_a = row.select_one('div.col_a.col.text')
        vocab = col_a.text
        col_b = row.select_one('div.col_b.col.text')
        meaning = col_b.text
        vocab_bag['vocab'].append(vocab)
        vocab_bag['meaning'].append(meaning)

    return level_name, vocab_bag


def get_lesson(url):
    lesson = dict()
    level_urls = get_level_urls(url)
    for level_url in level_urls:
        level_name, vocab_bag = get_level_vocab(level_url)
        lesson[level_name] = vocab_bag
    return lesson


def database_cloner(url, save_folder_path):
    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)
    save_path = os.path.join(save_folder_path, 'lesson.pkl')

    lesson = get_lesson(url)
    lesson = {'url': url, 'lesson': lesson}

    with open(save_path, 'wb') as f:
        pickle.dump(lesson, f, pickle.HIGHEST_PROTOCOL)

    print('Lesson saved at: ' + save_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=str, default='https://www.memrise.com/course/131661/sogang-korean-new-series-1b-vocabulary-2/')
    parser.add_argument('--save', type=str, default='../lesson/')
    args = parser.parse_args()

    database_cloner(args.root, args.save)
