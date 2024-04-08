from jtl_shop.testcase.classes.common.explprer_manager import ExplprerManager

# --
# ...
# --

class JtlShopPyTest_ExplorerManager():
    site_adress = "https://2-jtl-shop-p-a-7acf6a8f.docker.jtl-software.de"
    explprer_manager = ExplprerManager(site_adress=site_adress)

    @classmethod
    def run_browser(cls):
        assert cls.explprer_manager.run_browser()
        
    @classmethod
    def close_browser(cls):
        assert cls.explprer_manager.close_browser()
        
    @classmethod
    def forward_browser(cls):
        assert cls.explprer_manager.forward_browser()
    
    @classmethod
    def backward_browser(cls):
        assert cls.explprer_manager.backward_browser()
    
    @classmethod
    def alle_cookies_loschen(cls):
        assert cls.explprer_manager.alle_cookies_loschen()

    @classmethod
    def get_alle_cookies(cls):
        assert isinstance(cls.explprer_manager.get_alle_cookies(), tuple)