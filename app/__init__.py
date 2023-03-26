import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
from app.routes import ApiController

dotenv_path = '.env'
load_dotenv(dotenv_path)

port = int(os.environ.get("PORT"))
config_file_path = os.environ.get("CONFIG_FILE_PATH")
number_of_sections_to_randomize = int(os.environ.get("NUMBER_OF_SECTIONS_TO_RANDOMIZE"))
max_tests_number = int(os.environ.get("MAX_TESTS_NUMBER"))

controller = ApiController(config_file_path=config_file_path,
                           number_of_sections_to_randomize=number_of_sections_to_randomize,
                           max_tests_number=max_tests_number)
app = Flask(__name__)
controller.init_app(app)
app.run(debug=True, host="localhost", port=port)
