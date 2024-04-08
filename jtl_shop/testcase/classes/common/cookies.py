from jtl_shop.core.object_provider import ObjectProvider
from jtl_shop.core.base_jtl_shop import BaseJtlShop

# --
# ...
# --


class Cookies(BaseJtlShop):
    def __init__(self) -> None:
        self.elements = self.get_elements()

# --
# ...
# --

    def get_elements(self) -> str:
        return ObjectProvider()(__file__.replace('.py', '.json', -1))

# --
# ...
# --

    def akzeptiren_cookies_click(self) -> bool:

        try:

            self.find_element(self.elements.btn_akzeptiren).click()
            return True

        except Exception as exp:
            print(exp)
            return False

# --
# ...
# --

    def konfigurieren_cookies_click(self) -> bool:

        try:

            self.find_element(self.elements.btn_konfigurieren).click()
            return True

        except Exception as exp:
            print(exp)
            return False

# --
# ...
# --

    def ablehnen_cookies_click(self) -> bool:

        try:

            self.find_element(self.elements.btn_ablehnen).click()
            return True

        except Exception as exp:
            print(exp)
            return False