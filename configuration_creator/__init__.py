import os
import sys
import time
from threading import Thread
import webview
from flask import Flask
from .routes import ApiController
from .defaults import DEFAULT_PORT


class ConfigurationCreatorApp:

    def __init__(self):
        self._app = Flask(__name__)
        self._stop_thread = False
        self._host = "localhost"
        self._port = DEFAULT_PORT
        self._app_thread = None

    def run(self, config_file_path, max_tests_number, number_of_sections_to_randomize, port=DEFAULT_PORT, width=1200,
            height=800, ):
        if port < 0 or port > 65536:
            print("Port number needs to be positive, 0 to 65536,")
            self._stop_app()
            sys.exit(0)
        controller = ApiController(config_file_path, max_tests_number, number_of_sections_to_randomize)
        controller.init_app(self._app)
        self._app_thread = Thread(target=self._run_app)
        # https://stackoverflow.com/questions/49469978/properly-terminate-flask-web-app-running-in-a-thread
        self._app_thread.setDaemon(True)
        self._app_thread.start()
        self._start_webview(port, width, height)

    def _run_app(self, ):
        self._app.run(host=self._host, port=self._port)

    def _stop_app(self, ):
        sys.exit(0)

    def _start_webview(self, port, width, height):
        window = webview.create_window('Configuration Creator', f'http://{self._host}:{port}/', confirm_close=True,
                                       width=width, height=height, )
        window.events.closed += self._stop_app
        webview.start()
