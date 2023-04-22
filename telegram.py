import requests
import json
import configparser

tg_url = "https://api.telegram.org/bot"
file = 'config.ini'

# 创建配置文件对象
con = configparser.ConfigParser()

# 读取文件
con.read(file, encoding='utf-8')

# 获取所有section
bot = dict(con.items('bot'))


def send_message(photo_url, title):
    request_url = tg_url + bot['token'] + "/sendMessage"
    headers = {'Content-Type': 'application/json'}
    payload = {"chat_id": bot['chat_id'], "text": "[" + title + "](" + photo_url + ")", "parse_mode": "Markdown",
               "disable_notification": "true"}
    r = requests.post(request_url, headers=headers, data=json.dumps(payload))
    print(r)


def send_document(document_location):
    request_url = tg_url + bot['token'] + "/sendDocument"

    files = {'document': open(document_location, 'rb')}
    data = dict(chat_id=bot['chat_id'], disable_notification="true")
    print("Start Request Telegram APIS")
    r = requests.post(request_url, data=data, files=files)
    print(r)


def send_photo(photo_file, title):
    request_url = tg_url + bot['token'] + "/sendPhoto"
    data = dict(chat_id=bot['chat_id'],
                caption=title,
                parse_mode='Markdown')
    files = {'photo': open(photo_file, 'rb')}
    r = requests.post(request_url, data=data, files=files)
    print(r.text)
