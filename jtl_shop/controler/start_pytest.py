
# --
# ...
# --

# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# wd=webdriver.Chrome(service=Service("C:/OneDrive/Manager/WebDrivers/chromedriver.exe"))
# wd.get("https://2-jtl-shop-p-a-7acf6a8f.docker.jtl-software.de/search/?qs=G%C3%BCrtel")
# time.sleep(5)

# element = wd.find_element(By.CSS_SELECTOR,"#shop-nav > li.nav-item.dropdown.account-icon-dropdown > a > span")
# time.sleep(2)
# element.click()
# time.sleep(2)
# element = wd.find_element(By.ID,"email_quick")
# element.send_keys("sjdkfhdsjgh")
# time.sleep(2)
# element = wd.find_element(By.ID,"password_quick")
# time.sleep(2)
# element.send_keys('dakfugsdajkfgsjdafgsjkdafgjsd')
# h=0

# for item in elements:
#     print(item.text)

# module = "jtl_shop.testcase.szenarien.home_page_search_item"
# module = "jtl_shop.testcase.szenarien.artikel_in_wagenkorb_hinzufugen"

from jtl_shop.testcase.classes.common.explprer_manager import ExplprerManager
from jtl_shop.testcase.classes.common.cookies import Cookies
from jtl_shop.testcase.classes.pages.page_home.page_home import PageHome
from jtl_shop.testcase.classes.pages.page_home.form_login import FormLogin

# --
# ...
# --

class PyTest_Start:
    site_adress = "https://2-jtl-shop-p-a-7acf6a8f.docker.jtl-software.de"
    
    @classmethod
    def open_browser(cls):
        assert_value = True
        assert_value = assert_value and ExplprerManager(site_adress=cls.site_adress).run_browser()
        assert_value = assert_value and ExplprerManager(site_adress=cls.site_adress).alle_cookies_loschen()
        assert assert_value
        
    @classmethod
    def akzeptiren_cookies(cls):
        assert Cookies().akzeptiren_cookies_click()
        
    @classmethod
    def get_all_menus_name(cls):
        all_kategories_name = PageHome().get_all_menus_name()
        for kategories in all_kategories_name:
            print(kategories)
        assert isinstance(all_kategories_name, list)
        
    @classmethod
    def get_all_kategories_name(cls):
        all_kategories_name = PageHome().get_all_kategories_name()
        for kategories in all_kategories_name:
            print(kategories)
        assert isinstance(all_kategories_name, list)
        
    @classmethod
    def login_in_shop(cls):
        PageHome().to_login_form()
        assert FormLogin().logindata_eingeben()
        
    @classmethod
    def login_password_vergesen(cls):
        PageHome().to_login_form()
        assert FormLogin().login_password_vergesen()
        
    @classmethod
    def login_jetzt_registrieren(cls):
        PageHome().to_login_form()
        assert FormLogin().login_jetzt_registrieren()
        
    @classmethod
    def search_item_eingeben(cls):
        assert PageHome().search_item_eingeben(text='gürtel')
        