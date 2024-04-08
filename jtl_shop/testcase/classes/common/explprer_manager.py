from jtl_shop.core.object_provider import ObjectProvider
from jtl_shop.core.base_jtl_shop import BaseJtlShop

# --
# ...
# --


class ExplprerManager(BaseJtlShop):
    def __init__(self, site_adress: str = '') -> None:
        self.elements = self.get_elements()
        self.site_adress = site_adress

# --
# ...
# --

    def get_elements(self) -> str:
        return ObjectProvider()(__file__.replace('.py', '.json', -1))

# --
# ...
# --

    def run_browser(self) -> bool:
        
        try:
            
            return self.get(self.site_adress)

        except Exception as exp:
            print(exp)
            return False

# --
# ...
# --

    def close_browser(self) -> bool:
        
        try:
            
            return self.quit()

        except Exception as exp:
            print(exp)
            return False

# --
# ...
# --

    def forward_browser(self) -> bool:
        
        try:
            
            return self.forward()

        except Exception as exp:
            print(exp)
            return False

# --
# ...
# --

    def backward_browser(self) -> bool:
        
        try:
            
            return self.instance.backward()

        except Exception as exp:
            print(exp)
            return False
        
# --
# ...
# --

    def alle_cookies_loschen(self) -> bool:

        try:

            return self.delete_all_cookies()

        except Exception as exp:
            print(exp)
            return False

# --
# ...
# --

    def get_alle_cookies(self) -> tuple:

        try:

            all_cookies = self.get_all_cookies()
            print(all_cookies)
            return True, all_cookies

        except Exception as exp:
            print(exp)
            return False