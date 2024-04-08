from drivers.web.selenium_driver.core.base_selenium import BaseSelenium
from drivers.web.selenium_driver.config.selenium_config import SeleniumConfig
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from typing import Any
from drivers.web.selenium_driver.core.chain import Chain


class SeleniumDriver(BaseSelenium):
    def __init__(self) -> None:
        ...

# --
# ...
# --

    @classmethod
    def get_config_dictionary(cls):
        return SeleniumConfig().instance.dictionary

# --
# ... explorer
# --

    def quit(self) -> bool:

        try:

            self.driver.quit()
            return True

        except Exception as exp:
            print(exp)
            return False

    def get(self, url: str = "http://www.google.com") -> bool:

        try:

            self.driver.get(url)
            return True

        except Exception as exp:
            print(exp)
            return False

    def forward(self) -> bool:

        try:

            self.driver.forward()
            return True

        except Exception as exp:
            print(exp)
            return False

    def backward(self) -> bool:
        try:

            self.driver.back()
            self.delay(3)
            return True

        except Exception as exp:
            print(exp)
            return False

# --
# ...
# --

    def switch_driver_on_parent(self) -> bool:
        try:

            self.driver = self.driver.switch_to.default_content()
            return True

        except Exception as exp:
            print(exp)
            return False

# --
# ... find element
# --

    def find_elements(self, element: dict) -> list:

        try:

            key, value = element
            self.current_elements = self.driver.find_elements(key, value)
            return self.current_elements

        except Exception as exp:
            print(exp)
            return False

    def find_element(self, element: Any) -> Any:

        try:
            if isinstance(element, WebElement):
                self.current_element = element
                return self.current_element

            key, value = element
            self.current_element = self.driver.find_element(key, value)
            return self.current_element

        except Exception as exp:
            print(exp)
            return False

# --
# ... sen, set text
# --

    def send_keys(self, text="") -> bool:

        try:

            self.current_element.send_keys(text)
            return True

        except Exception as exp:
            print(exp)
            return False

    def set_text(self, element: dict, text: str, is_clear=True, is_enter=False, is_use_key=False, wait_for_object=10, delay=0.05) -> bool:

        try:

            try:

                self.wait_and_change_element(self).presence_of_element_located(
                    element, wait_for_secound=wait_for_object)

            except Exception as exp:
                print(exp)

            finally:
                self.find_element(element)

            self.delay(delay)

            if is_clear:
                self.current_element.clear()

            if is_enter:
                text += Keys.ENTER

            if is_use_key:
                for chr in text:
                    self.send_keys(chr)

            else:
                self.send_keys(text)

            self.delay(delay)
            return True

        except Exception as exp:
            print(exp)
            return False

# --
# ... clicks
# --

    def click(self, element: dict) -> bool:

        try:

            self.find_element(element)
            self.current_element.click()
            return True

        except Exception as exp:
            print(exp)
            return False

    def hover_then_click(self, element: dict) -> bool:

        try:

            self.find_element(element)
            ActionChains(self.driver).move_to_element(
                self.current_element).click().perform()

            return True

        except Exception as exp:
            print(exp)
            return False

# --
# ... cookies
# --

    def delete_all_cookies(self) -> bool:

        try:

            self.driver.delete_all_cookies()
            self.delay(3)
            return True

        except Exception as exp:
            print(exp)
            return False

    def get_all_cookies(self) -> tuple:

        try:

            list_alle_cookies = self.driver.get_cookies()
            return True, list_alle_cookies

        except Exception as exp:
            print(exp)
            return False

# --
# ... navbar
# --

    def gat_navbar_item(self, element: dict, is_return_elemnts=True, is_return_text=True) -> tuple:
        self.find_element(element)
        self.current_elements = self.current_element.find_elements(
            "tag name", "li")

        list_navbar_itemt = [
            navbar_item for navbar_item in self.current_elements if navbar_item.text != ""] if is_return_elemnts else []
        list_navbar_item_text = [
            navbar_item.text for navbar_item in self.current_elements if navbar_item.text != ""] if is_return_text else []

        return list_navbar_itemt, list_navbar_item_text

    def gat_menu_item(self, element: dict, is_return_elemnts=True, is_return_text=True) -> tuple:
        self.find_element(element)
        self.current_elements = self.current_element.find_elements(
            "tag name", "li")

        list_menu_itemt = [
            menu_item for menu_item in self.current_elements if menu_item.text != ""] if is_return_elemnts else []
        list_menu_item_text = [
            menu_item.text for menu_item in self.current_elements if menu_item.text != ""] if is_return_text else []

        return list_menu_itemt, list_menu_item_text

    def get_nasted_navbar_item(self, parent_elment, name) -> WebElement:
        elements, names = self.gat_navbar_item(parent_elment)

        if name in names:
            element = elements[names.index(name)]
            return element

        return None

# --
# ... action chains
# --

    def perform_action_chains(self, action_chain: Chain) -> bool:

        acs = ActionChains(self.driver, duration=500)
        for id, element_action in action_chain.chains.items():
            element, action = element_action
            self.find_element(element)

            # set operation
            if action == 'click':
                acs.click(self.current_element)

            elif action == 'move_to_element':
                acs.move_to_element(self.current_element)

        acs.perform()

    def move_on_navbar_kategory(self, navbar, name) -> bool:
        ...