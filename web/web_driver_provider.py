from drivers.web.selenium_driver.selenium_driver import SeleniumDriver
from drivers.core.base_driver import BaseDriver

#--
#...
#--

class WebDriverProvider(BaseDriver):
    def __init__(self) -> None:
        self.selenium_driver = SeleniumDriver().instance