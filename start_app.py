import os
import sys
import time
from threading import Thread
import webview

import os
from os.path import join, dirname
from dotenv import load_dotenv


# https://stackoverflow.com/questions/4646659/how-to-convert-the-django-web-application-into-the-desktop-application

def start_webview():
    dotenv_path = join(dirname(__file__), 'app/.env')
    load_dotenv(dotenv_path)

    port = os.environ.get("PORT")
    window = webview.create_window('Configuration Creator', f'http://127.0.0.1:{port}/', confirm_close=True, width=1200,
                                   height=800)
    webview.start()
    # window.events.closed += sys.exit()


def start_app():
    abspath = os.path.abspath(__file__)
    current_dir = os.path.dirname(abspath)
    os.chdir(current_dir)
    os.system("python main.py")  # runserver {}:{}".format('127.0.0.1', '8000'))


if __name__ == '__main__':
    Thread(target=start_app).start()
    start_webview()
