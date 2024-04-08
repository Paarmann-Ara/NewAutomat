from jtl_shop.core.object_provider import ObjectProvider
from jtl_shop.core.base_jtl_shop import BaseJtlShop


class FormLogin(BaseJtlShop):
    def __init__(self) -> None:
        self.elements = self.get_elements()

        self.wait_and_change_element(self).frame_to_be_available_and_switch_to_it(
            self.elements.form_login)

# --
# ...
# --

    def get_elements(self) -> str:
        return ObjectProvider()(__file__.replace('.py', '.json', -1))

# --
# ...
# --

    def logindata_eingeben(self, email: str = "jtl@hotmail.de", password: str = "jtl") -> bool:

        try:

            self.set_text(self.elements.txb_email, email, is_use_key=True)
            self.set_text(self.elements.txb_password,
                          password, is_use_key=True)
            self.click(self.elements.btn_anmelden)
            return True

        except Exception as exp:
            print(exp)

# --
# ...
# --

    def login_password_vergesen(self) -> bool:

        try:

            return self.click(self.elements.lnk_passwortvergessen)

        except Exception as exp:
            print(exp)

# --
# ...
# --

    def login_jetzt_registrieren(self) -> bool:

        try:

            return self.click(self.elements.lnk_jetztregistrieren)

        except Exception as exp:
            print(exp)
