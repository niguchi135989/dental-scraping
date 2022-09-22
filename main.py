import csv
import os
import requests
import re
import slackweb
import git
import shutil
import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession

HIDDEN_CATEGORY = 'マンガ'
result = []


def resub(text):
    return re.sub(r"[,.:;'\"\n]", "", text).strip()


def scraping_white_cross():
    r = requests.get('https://www.whitecross.co.jp/articles')
    soup = BeautifulSoup(r.text, 'html.parser')

    for news in soup.find(class_='main f_left').find_all(class_='unit_block_02'):
        category = resub(news.find(class_='label_contents').text)
        title = resub(news.find(class_='title').text)
        url = 'https://www.whitecross.co.jp' + news.find('a').get('href')
        writer = resub(news.find(class_='users').find(class_='wrap_sub').text)
        if category not in HIDDEN_CATEGORY:
            result.append([
                title,
                url,
                category,
                writer
            ])


def scraping_doctor_book():
    r = requests.get('https://academy.doctorbook.jp/contents')
    soup = BeautifulSoup(r.text, 'html.parser')

    for news in soup.find_all(class_='page_drvideo_list'):
        category = resub(news.find(class_='page_drvideo_episode').find('span').text)
        title = resub(news.find(class_='page_drvideo_episode').text)
        title = resub(title.removeprefix(category))
        url = 'https://academy.doctorbook.jp' + news.find('a').get('href')
        if news.find(class_='page_drvideo_dr') is None:
            writer = '-'
        else:
            writer = resub(news.find(class_='page_drvideo_dr').text)
        if category not in HIDDEN_CATEGORY:
            result.append([
                title,
                url,
                category,
                writer
            ])


def scraping_1d():
    session = HTMLSession()
    r = session.get('https://oned.jp/posts')
    r.html.render(timeout=20)

    for news in r.html.find('.scoped-post-list-item-inner'):
        category = 'ニュース'
        title = resub(news.find('.scoped-post-title')[0].text)
        url = news.find('.scoped-post-list-item-inner a')[0].attrs["href"]
        writer = resub(news.find('.scoped-post-author')[0].text)
        if HIDDEN_CATEGORY not in title:
            result.append([
                title,
                'https://oned.jp' + url,
                category,
                writer
            ])


def output_csv():
    with open('last_log.csv', 'w', newline='', encoding='utf_8') as file:
        writer = csv.writer(file)
        for row in last_result:
            writer.writerow(row)


def read_csv():
    if not os.path.exists('last_log.csv'):
        raise Exception('ファイルがありません。')
    if os.path.getsize('last_log.csv') == 0:
        raise Exception('ファイルの中身が空です。')
    csv_list = pd.read_csv('last_log.csv', header=None).values.tolist()
    return csv_list


def list_up_new_data():
    new_data = []
    for tmp in result:
        if tmp not in last_result:
            new_data.append(tmp)
            last_result.append(tmp)
    return new_data


def send_to_slack(text):
    slack = slackweb.Slack(url=os.environ["SLACK_WEBHOOK_URL"])
    slack.notify(text=text)


def send_to_slack_diff_list(diff_list):
    text = '記事の追加は下記の通り。\n'
    for tmp in diff_list:
        if len(tmp[3]) == '-':
            text += '[' + tmp[2] + ']' + tmp[0] + '\n' + tmp[1] + '\n'
        else:
            text += '[' + tmp[2] + ']' + tmp[0] + '(' + tmp[3] + ')\n' + tmp[1] + '\n'
    send_to_slack(text)


def data_update():
    repo = git.Repo()
    repo.git.commit('.', '-m', '\"Update Data\"')
    origin = repo.remote(name='origin')
    origin.push('master')


print('scraping white cross')
scraping_white_cross()

print('scraping id')
scraping_1d()

print('scraping doctor book')
scraping_doctor_book()

print('read last result csv')
last_result = read_csv()

print('check add news')
add_news = list_up_new_data()

if len(add_news) > 0:
    print('add news -> ' + str(len(add_news)))
    print('send slack')
#    send_to_slack_diff_list(add_news)

    print('output csv')
    output_csv()

    print('commit data')
    data_update()
else:
    print('no news')
#    send_to_slack('記事の追加はありませんでした。')
