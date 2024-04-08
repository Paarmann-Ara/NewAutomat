from jtl_shop.core.object_provider import ObjectProvider
from jtl_shop.core.base_jtl_shop import BaseJtlShop

#--
#...
#--

class PageResultSearch(BaseJtlShop):
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

    def label_suche_nach_text(self)->None:
        suche_nach_text = self.find_element(self.elements.suche_nach).text
        print(suche_nach_text)
        return suche_nach_text
#--
#...
#--

    def list_items_nach_suchen(self)->None:
        product_list = []
        temp_selenium_driver_products = self.find_element(self.elements.product_list)
        temp_selenium_driver_product_list = temp_selenium_driver_products.find_elements(*self.elements.product_item_in_product_list)
        
        for temp_selenium_driver_product in temp_selenium_driver_product_list:
            print(temp_selenium_driver_product.text)
            product_list.append(temp_selenium_driver_product.text)
            
        return product_list
    
#--
#...
#--

    def present_page_of_first_item_nach_suchen(self)->None:
        temp_selenium_driver_products = self.find_element(self.elements.product_list)
        temp_selenium_driver_product_list = temp_selenium_driver_products.find_elements(*self.elements.product_hyperlink_in_product_list)
        self.delay(2)
        temp_selenium_driver_product_list[0].click()
        return True
    
#--
#...
#--

    def present_page_item_nach_suchen(self, item)->None:
        
        try:
            
            temp_selenium_driver_products = self.find_element(self.elements.product_list)
            temp_selenium_driver_product_list = temp_selenium_driver_products.find_elements(*self.elements.product_item_in_product_list)
            
            for temp_selenium_driver_item in temp_selenium_driver_product_list:
                if temp_selenium_driver_item.text == item:
                    self.delay(3)
                    temp_selenium_driver_item.click()
                    self.delay(3)
                    return True
            
            return False
        
        except Exception as exp:
            print(exp)