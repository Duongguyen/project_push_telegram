from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from bs4 import BeautifulSoup

session = requests.Session()

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

base_domain = "http://vxvault.net/ViriList.php"


def get_news():
    list_news = []
    resp = session.get(url=base_domain, headers=headers)
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

    return list_news


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'xin chao {update.effective_user.first_name}')


def news(update: Update, context: CallbackContext) -> None:
    data = get_news()
    str1 = ""

    for item in data:
        str1 = "Date: " + item["date"] + "\n" + \
               "Url: " + item["url"] + "\n" + \
               "MD5: " + item["md5"] + "\n" + \
               "IP: " + item["ip"] + "\n" + \
               "Tools: " + item["tools"]
        update.message.reply_text(f'{str1}')


updater = Updater("YOUR_TOKEN")

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('news', news))

updater.start_polling()
updater.idle()

