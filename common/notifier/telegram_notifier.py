import requests
import yaml
import json
import os
import traceback

def send_message(message_text, user="admin"):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(dir_path+"/" + "config.yml", 'r') as stream:
        config = yaml.load(stream)

    chat_id = config['telegram_config']['user'][user]

    telegram_message_api = 'https://api.telegram.org/bot{}/'.format(config['telegram_config']['token'])

    params ="sendMessage?text={}&chat_id={}".format(message_text, chat_id)

    with requests.Session() as s:
        s.post(telegram_message_api + params)

