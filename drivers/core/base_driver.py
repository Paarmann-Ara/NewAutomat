from typing import Any
from abc import ABC, abstractmethod
import time


# --
# ...
# --
    
class BaseDriver(ABC):
    
# --
# ...
# --
   
    def __new__(cls, **kwargs: Any):
        if not hasattr(cls, 'instance'):        
            cls.instance = super().__new__(cls)
            
            cls.instance.config_dictionary = cls.get_config_dictionary()
            cls.instance.delay = cls.delay
                                          
        return cls.instance

# --
# ...
# --

    def __init__(self, *args, **kwargs: Any) -> None:
        pass    
    
# --
# ...
# --
    
    @classmethod
    def get_config_dictionary(cls) -> str:
            return ''
        
# --
# ...
# --
    
    @classmethod
    def delay(cls, delay = 1) -> str:
        time.sleep(delay)