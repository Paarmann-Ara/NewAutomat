from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class WaitAndChangeElement:
    def __init__(self, instance) -> None:
        self.instance = instance

# --
# ...
# --

    def presence_of_element_located(self, element: dict, wait_for_secound=2):

        try:

            key, value = element

            self.instance.current_element = WebDriverWait(self.instance.driver, wait_for_secound).until(
                expected_conditions.presence_of_element_located((key, value))
            )

            return True

        except Exception as exp:
            print(exp)
            return False

# --
# ...
# --

    def visibility_of_element_located(self, element: dict, wait_for_secound=2):

        try:

            key, value = element

            self.instance.current_element = WebDriverWait(self.instance.driver, wait_for_secound).until(
                expected_conditions.visibility_of_element_located((key, value))
            )

            return True

        except Exception as exp:
            print(exp)
            return False

# --
# ...
# --

    def presence_of_all_elements_located(self, element: dict, wait_for_secound=2):

        try:

            key, value = element

            self.instance.current_element = WebDriverWait(self.instance.driver, wait_for_secound).until(
                expected_conditions.presence_of_all_elements_located(
                    (key, value))
            )

            return True

        except Exception as exp:
            print(exp)
            return False

# --
# ...
# --

    def element_to_be_selected(self, element: dict, wait_for_secound=2):

        try:

            key, value = element

            self.instance.current_element = WebDriverWait(self.instance.driver, wait_for_secound).until(
                expected_conditions.element_to_be_selected((key, value))
            )

            return True

        except Exception as exp:
            print(exp)
            return False

# --
# ...
# --

    def element_to_be_clickable(self, element: dict, wait_for_secound=2):

        try:

            key, value = element

            self.instance.current_element = WebDriverWait(self.instance.driver, wait_for_secound).until(
                expected_conditions.element_to_be_clickable((key, value))
            )

            return True

        except Exception as exp:
            print(exp)
            return False

# --
# ...
# --

    def visibility_of(self, element: dict, wait_for_secound=2):

        try:

            key, value = element

            self.instance.current_element = WebDriverWait(self.instance.driver, wait_for_secound).until(
                expected_conditions.visibility_of((key, value))
            )

            return True

        except Exception as exp:
            print(exp)
            return False

# --
# ...
# --

    def element_located_to_be_selected(self, element: dict, wait_for_secound=2):

        try:

            key, value = element

            self.instance.current_element = WebDriverWait(self.instance.driver, wait_for_secound).until(
                expected_conditions.element_located_to_be_selected(
                    (key, value))
            )

            return True

        except Exception as exp:
            print(exp)
            return False

# --
# ...
# --

    def frame_to_be_available_and_switch_to_it(self, element: dict, wait_for_secound=2) -> bool:

        try:

            key, value = element

            self.instance.current_element = WebDriverWait(self.instance.driver, wait_for_secound).until(
                expected_conditions.frame_to_be_available_and_switch_to_it(
                    (key, value))
            )
            return True

        except Exception as exp:
            print(exp)
            return False
