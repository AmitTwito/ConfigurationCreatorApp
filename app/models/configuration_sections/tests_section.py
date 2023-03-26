from app.enums.configuration_section_enum import ConfigurationSections
from app.models.configuration_sections.configuration_section import ConfigurationSection


class TestsSection(ConfigurationSection):

    def __init__(self, configuration_section_type: ConfigurationSections, template_file: str, max_tests_number: int):
        super().__init__(configuration_section_type, template_file)
        self._tests = []
        self._max_tests_number = max_tests_number
        self._form_keys = [{"key": "selected-tests", "is_collection": True}]

    def validate(self, tests: []):
        if not tests:
            return []

        error = "Error at updating the tests list: "
        there_any_error = False

        if len(tests) > self._max_tests_number:
            error += f"The number of tests is greater than the max number of tests which is {self._max_tests_number}. "
            there_any_error = True
        try:
            tests = [int(test) for test in tests]
        except ValueError:
            error += "The list of tests need to be of positive integers."
            there_any_error = True

        if any(test not in range(1, self._max_tests_number + 1) for test in tests):
            error += "Test numbers need to be within range 1 to {self._max_tests_number}. "
            there_any_error = True

        if there_any_error:
            return {"error": error}
        return tests

    def validate_from_yaml(self, tests: []):
        if not tests:
            return []

        error = "Error at updating the tests list: "
        there_any_error = False
        if not all(isinstance(x, int) for x in tests):
            error += "The list of tests need to be of positive integers. "
            there_any_error = True

        if len(tests) > self._max_tests_number:
            error += f"The number of tests is greater than the max number of tests which is {self._max_tests_number}. "
            there_any_error = True

        try:
            tests = [int(test) for test in tests]
        except ValueError:
            error += "The list of tests need to be of positive integers."
            there_any_error = True

        if any(test not in range(1, self._max_tests_number + 1) for test in tests):
            error += "Test numbers need to be within range 1 to {self._max_tests_number}. "
            there_any_error = True

        if there_any_error:
            return {"error": error}
        return tests

    def update(self, tests: []):
        self._tests = tests

    def as_dict(self) -> dict:
        return {'tests': self._tests}
