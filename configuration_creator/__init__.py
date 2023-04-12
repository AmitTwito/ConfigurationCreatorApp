import os
import sys
from threading import Thread
import webview
from flask import Flask
from .routes import Controller
from .defaults import DEFAULT_CONFIG_PATH, DEFAULT_MAX_TESTS_NUMBER, DEFAULT_RANDOM_SECTIONS_NUMBER
from screeninfo import get_monitors
import socket

os.environ['WEBVIEW2_USER_DATA_FOLDER'] = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'EdgeWebView')


def find_open_port_for_app():
    # https://stackoverflow.com/questions/5085656/how-to-select-random-port-number-in-flask
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def get_width_and_height_of_window_by_resolution_of_user():
    m = get_monitors()[0]
    return int(m.width * 0.5), int(m.height * 0.7)


class ConfigurationCreatorApp:

    def __init__(self, max_tests_number=DEFAULT_MAX_TESTS_NUMBER,
                 number_of_sections_to_randomize=DEFAULT_RANDOM_SECTIONS_NUMBER, config_file_path=DEFAULT_CONFIG_PATH,
                 is_verbose=True, ):

        self._port = find_open_port_for_app()
        self._host = "localhost"

        self._width, self._height = get_width_and_height_of_window_by_resolution_of_user()

        self._controller = Controller(self.close_application_window, config_file_path, max_tests_number,
                                      number_of_sections_to_randomize, is_verbose=is_verbose)

        self._app = Flask(__name__)
        self._controller.init_app(self._app)

    def run(self, ):
        # https://stackoverflow.com/questions/49469978/properly-terminate-flask-web-app-running-in-a-thread
        self._app_thread = Thread(target=self._run_app)
        self._app_thread.setDaemon(True)
        self._app_thread.start()
        self.open_application_window()
        return self._controller.get_configuration_data()

    def _run_app(self, ):
        try:
            self._app.run(host=self._host, port=self._port)
        except Exception as e:
            self.close_application_window()
            raise e

    def open_application_window(self, ):
        self._window = webview.create_window('Configuration Creator', f'http://{self._host}:{self._port}/',
                                             width=self._width, height=self._height, )
        webview.start()

    def close_application_window(self):
        self._window.destroy()
