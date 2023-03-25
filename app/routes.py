from app import app
from app.models.logger import LogType
from flask import render_template, request, redirect

from app.models.business_logic import BuisinessLogic

n = 4
bl = BuisinessLogic(number_of_sections_to_randomize=n)


@app.route('/')
def index():
    return render_template('index.html', state=bl.get_state())


@app.route('/last_configurations', methods=["GET", "POST"])
def last_configurations():
    if request.method == "POST":
        try:
            bl.update_config(is_randomized_sections=True, request_form=request.form)
            bl.save_config_to_file()
            return render_template('last_configurations.html', state=bl.get_state())
        # except ValueError as e:
        #     state.add_log(str(e), LogType.ERROR)
        #     return redirect('/')
        # except FileNotFoundError as e:
        #     state.add_log(str(e), LogType.ERROR)
        #     return redirect('/')

        except Exception as e:  # all other exceptions
            print('Error on POST request /last_configurations: ')
            bl.add_log(f"{str(e)}", LogType.ERROR)
            return redirect('/')
    else:
        return render_template('last_configurations.html', state=bl.get_state())


@app.route('/finish', methods=["POST"])
def finish():
    try:
        bl.update_config(is_randomized_sections=False, request_form=request.form)
        bl.save_config_to_file()
    # except ValueError as e:
    #     state.add_log(str(e), LogType.ERROR)
    #     return redirect('/')
    except Exception as e:
        print('Error on POST request /finish: ')
        bl.add_log(f"{str(e)}", LogType.ERROR)

    return redirect('/last_configurations')


@app.route('/users/delete/<user_id>', methods=["DELETE"])
def delete_user(user_id):
    return redirect(bl.delete_user(user_id))


@app.route('/users/add', methods=["POST"])
def add_user():
    user_type = request.form.get('selected-user-type')
    email = request.form.get('new-user-email')
    password = request.form.get('new-user-password')
    to_current_page = bl.add_user(user_type, email, password)
    return redirect(to_current_page)
