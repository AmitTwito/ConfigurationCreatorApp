from app import app
from flask import render_template, url_for, request, redirect

from app.models.configuration import Configuration
from app.models.state import State

n = 4
state = State(sections_number=n)


@app.route('/')
def index():

    return render_template('index.html', state=state.to_dict())


# @app.route('/')
# def index():
#     n = 3
#     state.generate_random_sections(3)
#     return render_template('index.html', title="Configuration Creator", state=state,
#                            debug_checked=config.is_production_mode)

@app.route('/last_configurations', methods=["GET", "POST"])
def last_configurations():
    next_page = None
    if 'test' in request.form:
        checkes = request.form['test']
    if 'toggle' in request.form:
        toggle = ''
    state.config.save_to_file()
    next_page = render_template('last_configurations.html', state=state.to_dict())
    return next_page


@app.route('/users/delete/<user_id>')
def delete_user(user_id):
    user_id = int(user_id) - 1

    try:
        del state.config.users[user_id]
    except Exception:
        state.add_log(f"Error deleting user with id {user_id}")
    if "users_table.html" in state.random_sections:
        return redirect('/')
    else:
        return redirect('/last_configurations')


@app.route('/users/add', methods=["POST"])
def add_user():
    return redirect('/')

@app.route('/tests/change_all_tests')
def change_all_tests():
    state.change_selected_tests()

    return
# @app.route('/last_configurations')
# def back():
#     return render_template('last_configurations.html', title="Configuration Creator", state=state)
