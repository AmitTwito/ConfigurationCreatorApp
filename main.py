from configuration_creator import ConfigurationCreatorApp

port = 5000  # int(os.environ.get("PORT"))
config_file_path = "config.yaml"  # os.environ.get("CONFIG_FILE_PATH")
number_of_sections_to_randomize = 3  # int(os.environ.get("NUMBER_OF_SECTIONS_TO_RANDOMIZE"))
max_tests_number = 10  # int(os.environ.get("MAX_TESTS_NUMBER"))

configuration_creator_app = ConfigurationCreatorApp()
configuration_creator_app.run(config_file_path=config_file_path, max_tests_number=max_tests_number,
                              number_of_sections_to_randomize=number_of_sections_to_randomize, port=port, width=1200,
                              height=800, )
