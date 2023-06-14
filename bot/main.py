import threading

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from bs4 import BeautifulSoup
import time

session = requests.Session()

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

url_vault = "http://vxvault.net/ViriList.php"
url_bazaar = "https://bazaar.abuse.ch/statistics/"
url_blocklist = "https://www.blocklist.de/en/partners.html"


def get_news(update: Update, sleepTime):
    list_news = []
    resp = session.get(url=url_vault, headers=headers)
    soups = BeautifulSoup(resp.text, "html.parser")
    tr_data = soups.find_all('tr')
    if resp.status_code == 200:
        for row in tr_data[1:]:
            newdict = {}
            td_list = row.find_all('td')
            newdict["date"] = td_list[0].find_all("a")[0].text.strip()
            newdict["url"] = td_list[1].text.strip()
            newdict["md5"] = td_list[2].find_all("a")[0].text.strip()
            newdict["ip"] = td_list[3].find_all("a")[0].text.strip()
            newdict["tools"] = td_list[4].find_all("a")[0].text + " " + td_list[4].find_all("a")[1].text
            list_news.append(newdict)

    for item in list_news:
        str1 = "Date: " + item["date"] + "\n" + \
               "Url: " + item["url"] + "\n" + \
               "MD5: " + item["md5"] + "\n" + \
               "IP: " + item["ip"] + "\n" + \
               "Tools: " + item["tools"]

        update.message.reply_text(f'{str1}')
        time.sleep(sleepTime)


def get_bazaar(update: Update, sleepTime):
    list_news = []
    resp = session.get(url=url_bazaar, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")
    tr_data = soup.find_all('tr')
    for row in tr_data[1:16]:
        newdict = {}
        td_list = row.find_all('td')
        if td_list:
            newdict["rank"] = td_list[0].text
            newdict["reporter"] = td_list[1].find_all("a")[0].text
            newdict["last_activity"] = td_list[2].text
            newdict["submissions"] = td_list[3].text + ""
            list_news.append(newdict)

    for item in list_news:
        str1 = "Rank: " + item["rank"] + "\n" + \
               "Reporter: " + item["reporter"] + "\n" + \
               "Last Activity: " + item["last_activity"] + "\n" + \
               "Submissions: " + item["submissions"]

        update.message.reply_text(f'{str1}')
        time.sleep(sleepTime)


def get_blocklist(update: Update, sleepTime):
    list_news = []
    response = requests.get(url=url_blocklist, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    tr_data = soup.find_all('tr')
    for row in tr_data[1:]:
        newdict = {}
        td_list = row.find_all('td')
        newdict["name"] = td_list[0].find_all("a")[0].text
        newdict["server"] = td_list[1].text.split('\n')[1].strip()
        newdict["since"] = td_list[2].text.split('\n')[1].strip()
        newdict["donated"] = td_list[3].text.split('\n')[1].strip()
        list_news.append(newdict)

    for item in list_news:
        str1 = "Name: " + item["name"] + "\n" + \
               "Server: " + item["server"] + "\n" + \
               "Since: " + item["since"] + "\n" + \
               "Donated: " + item["donated"]

        update.message.reply_text(f'{str1}')
        time.sleep(sleepTime)


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'xin chao {update.effective_user.first_name}')


def news(update: Update, context: CallbackContext):
    thread2 = threading.Thread(target=get_bazaar, args=(update, 5))
    thread2.start()

    thread1 = threading.Thread(target=get_news, args=(update, 5))
    thread1.start()

    thread3 = threading.Thread(target=get_blocklist, args=(update, 5))
    thread3.start()


updater = Updater("6185338495:AAGeRNqn8kZdrwlP2CRCFeIMMqr_3guL1jo")

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('news', news))

updater.start_polling()
updater.idle()

