import os
import sys
import time
from threading import Thread
import webview

import os
from os.path import join, dirname
from dotenv import load_dotenv

# https://stackoverflow.com/questions/4646659/how-to-convert-the-django-web-application-into-the-desktop-application

stop_app = False


def start_webview():
    dotenv_path = join(dirname(__file__), 'app/.env')
    load_dotenv(dotenv_path)

    port = os.environ.get("PORT")
    if int(port) < 0 or int(port) > 65536:
        print("Port number needs to be positive, 0 to 65536,")
        sys.exit(0)
    window = webview.create_window('Configuration Creator', f'http://localhost:{port}/', confirm_close=True, width=1200,
                                   height=800, )
    # window.events.closed += sys.exit()
    # window.events.closed += set_stop()
    webview.start()


def set_stop():
    stop_app = True


def start_app():
    abspath = os.path.abspath(__file__)
    current_dir = os.path.dirname(abspath)
    os.chdir(current_dir)
    os.system("python main.py")  # runserver {}:{}".format('127.0.0.1', '8000'))

    # while not stop_app:
    #     time.sleep(0.5)


if __name__ == '__main__':
    t = Thread(target=start_app)
    t.start()
    start_webview()
    #t.join()
