import os
import sys
import time
from threading import Thread
import webview


# https://stackoverflow.com/questions/4646659/how-to-convert-the-django-web-application-into-the-desktop-application

def start_webview():
    window = webview.create_window('Configuration Creator', 'http://localhost:5000/', confirm_close=True, width=1200,
                                   height=800)
    webview.start()
    #window.closed = os.()


def start_app():
    abspath = os.path.abspath(__file__)
    current_dir = os.path.dirname(abspath)
    os.chdir(current_dir)
    if sys.platform in ['win32', 'win64']:
        os.system("python main.py")  # runserver {}:{}".format('127.0.0.1', '8000'))
        print("here")
        # time.sleep(10)
    else:
        os.system("python3 main.py")  # runserver {}:{}".format('127.0.0.1', '8000'))
        # time.sleep(10)


if __name__ == '__main__':
    Thread(target=start_app).start()
    start_webview()
