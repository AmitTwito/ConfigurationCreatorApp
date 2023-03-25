from app import app
from app.models.logger import LogType
from flask import render_template, url_for, request, redirect

from app.models.configuration import Configuration
from app.models.state import State

n = 4
state = State(sections_number=n)


@app.route('/')
def index():
    return render_template('index.html', state=state.as_dict())


@app.route('/last_configurations', methods=["GET", "POST"])
def last_configurations():
    if request.method == "POST":
        try:
            for config_section in state.random_sections:
                config_section_update_function = state.config_section_to_function[config_section]
                config_section_update_function(request.form)
            state.save_config_to_file()
            return render_template('last_configurations.html', state=state.as_dict())
        # except ValueError as e:
        #     state.add_log(str(e), LogType.ERROR)
        #     return redirect('/')
        # except FileNotFoundError as e:
        #     state.add_log(str(e), LogType.ERROR)
        #     return redirect('/')
        except Exception as e:
            state.add_log(f"Error on POST request /last_configurations: {str(e)}", LogType.ERROR)
            return redirect('/')
    else:
        return render_template('last_configurations.html', state=state.as_dict())


@app.route('/finish', methods=["POST"])
def finish():
    try:
        for config_section in state.rest_of_the_sections:
            config_section_update_function = state.config_section_to_function[config_section]
            config_section_update_function(request.form)
        state.save_config_to_file()
    # except ValueError as e:
    #     state.add_log(str(e), LogType.ERROR)
    #     return redirect('/')
    except Exception as e:
        state.add_log(f"Error on POST request /finish: {str(e)}", LogType.ERROR)

    return redirect('/last_configurations')


@app.route('/users/delete/<user_id>', )
def delete_user(user_id):
    return redirect(state.delete_user(user_id))


@app.route('/users/add', methods=["POST"])
def add_user():
    user_type = request.form.get('selected-user-type')
    email = request.form.get('new-user-email')
    password = request.form.get('new-user-password')
    to_current_page = state.add_user(user_type, email, password)
    return redirect(to_current_page)
