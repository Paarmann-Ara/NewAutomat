from jtl_shop.testcase.classes.pages.page_home.form_login import FormLogin
from jtl_shop.testcase.classes.common.explprer_manager import ExplprerManager
from jtl_shop.core.object_provider import ObjectProvider
from jtl_shop.core.base_jtl_shop import BaseJtlShop


class PageHome(BaseJtlShop):
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

    def get_all_menus_name(self) -> list:
        _, menus_name = self.gat_menu_item(self.elements.header_menu)
        return menus_name

# --
# ...
# --

    def get_all_menus_item(self) -> list:
        _, menus_item = self.gat_menu_item(self.elements.header_menu)
        return menus_item

# --
# ...
# --

    def get_all_kategories_element_name(self) -> tuple:
        return self.gat_navbar_item(self.elements.nav_kategories)

# --
# ...
# --

    def click_on_kategory(self, name) -> bool:
        element = self.get_nasted_navbar_item(self.elements.nav_kategories, name)
        
        self.action_chain.chains = (element, self.action.move_to_element)
        self.action_chain.chains = (element, self.action.click)
        self.perform_action_chains(self.action_chain)
        
# --
# ...
# --

    def click_on_nasted_kategory(self, parent, child) -> bool:
        element = self.get_nasted_navbar_item(self.elements.nav_kategories, parent)
        self.action_chain.chains = (element, self.action.move_to_element)
        
        element = self.get_nasted_navbar_item(self.elements.nav_kategories, child)
        self.action_chain.chains = (element, self.action.move_to_element)
        self.action_chain.chains = (element, self.action.click)
        self.perform_action_chains(self.action_chain)
        
# --
# ...
# --

    def search_item_eingeben(self, text: str = "Gürtel") -> bool:
        return self.set_text(self.elements.txb_search, text=text, is_use_key=True, is_enter=True)

# --
# ...
# --

    def to_login_form(self) -> bool:
        # self.hover_then_click(self.elements.btn_user)

        self.action_chain.chains = (self.elements.btn_user, self.action.click)
        self.perform_action_chains(self.action_chain)


ExplprerManager(
    site_adress="https://2-jtl-shop-p-a-7acf6a8f.docker.jtl-software.de").run_browser()
PageHome().click_on_kategory('_')
PageHome().click_on_nasted_kategory('_', 'Angebot')
