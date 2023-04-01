from configuration_creator.enums.configuration_section_enum import ConfigurationSections
from configuration_creator.business_logic import BusinessLogic
from configuration_creator.models.logger import LogTypes
from flask import render_template, request, redirect

from utils.errors.value_validation_error import ValueValidationError


class ApiController:

    def __init__(self, config_file_path=None, max_tests_number=None,
                 number_of_sections_to_randomize=None):
        self.bl = BusinessLogic(config_file_path=config_file_path,
                                number_of_sections_to_randomize=number_of_sections_to_randomize,
                                max_tests_number=max_tests_number, )

    def init_app(self, app):

        @app.route('/')
        def index():
            return render_template('index.html', state=self.bl.get_state())

        @app.route('/last_configurations', methods=["GET", "POST"])
        def last_configurations():
            if request.method == "POST":
                try:
                    self.bl.validate_and_update_config(is_randomized_sections=True, request_form=request.form)
                    self.bl.save_config_to_file()
                    return render_template('last_configurations.html', state=self.bl.get_state())
                except ValueValidationError as e:
                    return redirect('/')
                except Exception as e:
                    print('Error on POST request /last_configurations: ')
                    self.bl.add_log(f"{str(e)}", LogTypes.ERROR, ex=e)
                    return redirect('/')
            else:
                return render_template('last_configurations.html', state=self.bl.get_state())

        @app.route('/finish', methods=["POST"])
        def finish():
            is_randomized_sections = False
            if self.bl.number_of_sections_to_randomize == len(ConfigurationSections):
                is_randomized_sections = True
            try:
                self.bl.validate_and_update_config(is_randomized_sections=is_randomized_sections,
                                                   request_form=request.form)
                self.bl.save_config_to_file()
            except Exception as e:
                print('Error on POST request /finish: ')
                self.bl.add_log(f"{str(e)}", LogTypes.ERROR, ex=e)

            return redirect('/last_configurations') if 0 < self.bl.number_of_sections_to_randomize < len(
                ConfigurationSections) else redirect('/')

        @app.route('/users/delete/<user_id>')
        def delete_user(user_id):
            return redirect(self.bl.delete_user(user_id))

        @app.route('/users/add', methods=["POST"])
        def add_user():
            user_type = request.form.get('selected-user-type')
            email = request.form.get('new-user-email')
            password = request.form.get('new-user-password')
            to_current_page = self.bl.add_user(user_type, email, password)
            return redirect(to_current_page)
