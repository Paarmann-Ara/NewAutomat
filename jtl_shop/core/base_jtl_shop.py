from typing import Any
from abc import ABC, abstractmethod
from drivers.web.web_driver_provider import WebDriverProvider
from drivers.web.selenium_driver.core.chain import Chain
from collections import namedtuple


class BaseJtlShop(ABC):

    def __new__(cls, **kwargs: Any):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)

            cls.instance.config_dictionary = cls.get_config_dictionary()
            cls.instance.elements = cls.instance.get_elements()

            cls.action_chain = Chain()
            _actions = ['click' ,'double_click' ,'context_click' ,'click_and_hold' ,'drag_and_drop' ,'key_down' ,'key_up' ,'release' ,'move_to_element' ,'send_keys' ,'send_keys_to_element' ,'scroll_to_element' ,'perform' ,'reset_actions']
            #cls.action = namedtuple('action', _actions)(*tuple(_actions))
            cls.action = namedtuple('action', ['click' ,'double_click' ,'context_click' ,'click_and_hold' ,'drag_and_drop' ,'key_down' ,'key_up' ,'release' ,'move_to_element' ,'send_keys' ,'send_keys_to_element' ,'scroll_to_element' ,'perform' ,'reset_actions'])(*tuple(_actions))

            temp_selenium_driver = WebDriverProvider().selenium_driver

            for methode in dir(temp_selenium_driver):
                if (methode[0:1] != '_') and (methode[0:2] != '__'):
                    setattr(cls.instance, methode, getattr(
                        temp_selenium_driver, methode))

        return cls.instance

# --
# ...
# --

    def __init__(self, *args, **kwargs: Any) -> None:
        pass

# --
# ...
# --

    @classmethod
    def get_config_dictionary(cls) -> str:
        return None

# --
# ...
# --

    @classmethod
    def get_elements(cls) -> str:
        return None
