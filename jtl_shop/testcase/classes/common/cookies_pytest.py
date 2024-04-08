from jtl_shop.core.base_jtl_shop import BaseJtlShop
from jtl_shop.testcase.classes.common.cookies import Cookies

# --
# ...
# --

class JtlShopPyTest_Cookies(BaseJtlShop):
    
    @classmethod
    def akzeptiren_cookies_click(cls):
        assert Cookies.akzeptiren_cookies_click()
        
    @classmethod
    def konfigurieren_cookies_click(cls):
        assert Cookies.konfigurieren_cookies_click()

    @classmethod
    def ablehnen_cookies_click(cls):
        assert Cookies.ablehnen_cookies_click()