import os
import sys
from threading import Thread
import webview
from flask import Flask
from .routes import Controller
from .defaults import DEFAULT_PORT

os.environ['WEBVIEW2_USER_DATA_FOLDER'] = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'EdgeWebView')


class ConfigurationCreatorApp:

    def __init__(self, config_file_path, max_tests_number, number_of_sections_to_randomize, port=DEFAULT_PORT,
                 width=1200, height=800, ):
        if port < 1024 or port > 65536:
            print("ERROR: Port number needs to be positive, 1024 to 65536", file=sys.stderr)
            sys.exit(0)
        self._port = port
        self._host = "localhost"

        self._width = width
        self._height = height

        self._app = Flask(__name__)

        self._controller = Controller(config_file_path, max_tests_number, number_of_sections_to_randomize)
        self._controller.init_app(self._app)

        # https://stackoverflow.com/questions/49469978/properly-terminate-flask-web-app-running-in-a-thread
        self._app_thread = Thread(target=self._run_app)
        self._app_thread.setDaemon(True)

    def run(self, ):
        self._app_thread.start()
        self._start_webview(self._port, self._width, self._height)
        return self._controller.get_configuration_data()

    def _run_app(self, ):
        try:
            self._app.run(host=self._host, port=self._port)
        except Exception as e:
            print(
                f"\nERROR: The port {self._port} is not valid, or not available.\n", file=sys.stderr)
            self._window.destroy()

    def _stop_app(self, ):
        sys.exit(0)

    def _start_webview(self, port, width, height):
        self._window = webview.create_window('Configuration Creator', f'http://{self._host}:{port}/',
                                             width=width, height=height)
        self._window.events.closed += self._stop_app
        webview.start()
