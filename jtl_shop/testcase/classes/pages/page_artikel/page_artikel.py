from jtl_shop.core.object_provider import ObjectProvider
from jtl_shop.core.base_jtl_shop import BaseJtlShop

#--
#...
#--

class PageArtikel(BaseJtlShop):
    def __init__(self) -> None:
        self.elements = self.get_elements()
    
# --
# ...
# --
    
    def get_objects(self) -> str:
        return ObjectProvider()(__file__.replace('.py','.json', -1))

#--
#...
#--

    def Artikel_in_warenkorb_hinzufugen(self, number_of_artikel_zu_hinzugugen = 2):
        for _ in range(number_of_artikel_zu_hinzugugen):
            self.click_(self.elements.btn_plus_in_warenkorb)
        
PageArtikel().Artikel_in_warenkorb_hinzufugen(5)