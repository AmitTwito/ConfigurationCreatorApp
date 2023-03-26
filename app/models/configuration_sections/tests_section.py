from app.enums.configuration_section_enum import ConfigurationSections
from app.models.configuration_sections.configuration_section import ConfigurationSection


class TestsSection(ConfigurationSection):

    def __init__(self, configuration_section_type: ConfigurationSections, template_file: str, max_tests_number: int):
        super().__init__(configuration_section_type, template_file)
        self._tests = []
        self._max_tests_number = max_tests_number

    def validate(self, tests: []):
        pass

    def validate_from_yaml(self, tests):
        error = ""
        if len(set(tests)) > self._max_tests_number:
            error += f"\nThe number of tests is greater than the max number of tests which is {self._max_tests_number - 1}"
        if [test not in range(1, self._max_tests_number + 1) for test in tests]:
            error += f"\nTest numbers need to be within range 1 to {self._max_tests_number - 1}"
        if error != "":
            return {"error": error}
        return tests

    def update(self, tests: []):
        self._tests = tests

    def as_dict(self) -> dict:
        return {'tests': self._tests}
