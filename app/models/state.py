from enum import Enum
import random


class ConfigurationSections(Enum):
    MODE = 1
    TESTS = 2
    USERS = 3
    REPORT_BACKGROUND_IMAGE = 4
    HARDWARE_ACCELERATION = 5


class State:
    def __init__(self, config):
        self.random_sections, self.rest_of_the_sections = [], []
        self.config = config
        self.messages = ["Configuration Creator V1", "Please make sure to insert correct inputs", 1, 2, 3, 54]
        self.config_section_to_template = {ConfigurationSections.MODE: "mode.html",
                                           ConfigurationSections.TESTS: "tests.html",
                                           ConfigurationSections.USERS: "users_table.html",
                                           ConfigurationSections.REPORT_BACKGROUND_IMAGE: "report_background_image.html",
                                           ConfigurationSections.HARDWARE_ACCELERATION: "hardware_acceleration.html",
                                           }

    def generate_random_sections(self, number_of_sections):
        if number_of_sections > 5:
            raise Exception("Number of sections to present needs to be 5 or less")
        section_numbers = random.sample(range(1, 6), number_of_sections)
        section_numbers.sort()
        self.random_sections = [self.config_section_to_template[ConfigurationSections(i)] for i in section_numbers]
        self.rest_of_the_sections = list(set(self.config_section_to_template.values()) - set(self.random_sections))

    def add_message(self, error):
        self.messages.append(error)
