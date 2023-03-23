from app import app
from flask import render_template, url_for,request

from app.models.configuration import Configuration
from app.models.state import State

config = Configuration()
state = State(config)


@app.route('/')
def index():
    n = 5
    state.generate_random_sections(n)
    return render_template('index.html', title="Configuration Creator", state=state,
                           debug_checked=config.is_production_mode)

# @app.route('/')
# def index():
#     n = 3
#     state.generate_random_sections(3)
#     return render_template('index.html', title="Configuration Creator", state=state,
#                            debug_checked=config.is_production_mode)


@app.route('/save_configuration', methods=["POST"])
def save_configuration():
    config.save_to_file()
    checkes = request.form['check']
    return render_template('')

def back():
    return