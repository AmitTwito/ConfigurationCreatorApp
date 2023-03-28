import os
import sys
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
from app.routes import ApiController

dir_name = os.path.dirname(__file__)
dotenv_path = join(dir_name, '.env')
load_dotenv(dotenv_path)

port = int(os.environ.get("PORT"))
config_file_path = os.environ.get("CONFIG_FILE_PATH")
number_of_sections_to_randomize = int(os.environ.get("NUMBER_OF_SECTIONS_TO_RANDOMIZE"))
max_tests_number = int(os.environ.get("MAX_TESTS_NUMBER"))

if port < 0 or port > 65536:
    print("Port number needs to be positive, 0 to 65536,")
    sys.exit(0)
if max_tests_number < 0:
    print("Max tests number needs to be positive.")
    sys.exit(0)

controller = ApiController(config_file_path=config_file_path,
                           number_of_sections_to_randomize=number_of_sections_to_randomize,
                           max_tests_number=max_tests_number)
app = Flask(__name__)
controller.init_app(app)
app.run(debug=True, host="localhost", port=port)

# webbrowser.get(using="google-chrome").open(f"http://localhost:{port}",new=0)
