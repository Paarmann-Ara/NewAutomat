from typing import Any
from jtl_shop.core.jtlshop_config import JtlShopConfig
 
#--
#...
#-- 

class ObjectProvider():
    def __init__(self, *args: Any) -> None:
        pass
    
#--
#...
#-- 

    def __call__(self, *args: Any) -> Any:
        for key,value in JtlShopConfig(*args).instance.dictionary.items():
            setattr(self, key, *value.items())
        return self
