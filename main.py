from configuration_creator import ConfigurationCreatorApp

if __name__ == '__main__':
    config_file_path = "config.yaml"
    number_of_sections_to_randomize = 3
    max_tests_number = 10

    configuration_creator_app = ConfigurationCreatorApp(max_tests_number, number_of_sections_to_randomize,
                                                        config_file_path=config_file_path, is_verbose=False, )

    data = configuration_creator_app.run()

    print(data)


