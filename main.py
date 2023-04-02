from configuration_creator import ConfigurationCreatorApp

if __name__ == '__main__':
    port = 5000
    config_file_path = "config.yaml"
    number_of_sections_to_randomize = 3
    max_tests_number = 10

    configuration_creator_app = ConfigurationCreatorApp(config_file_path=config_file_path,
                                                        max_tests_number=max_tests_number,
                                                        number_of_sections_to_randomize=number_of_sections_to_randomize,
                                                        port=port, width=1200,
                                                        height=800, )
    data = configuration_creator_app.run()
    print(data)
