from typing import Any
from abc import ABC, abstractmethod


# --
# ...
# --
    
class BaseFTP(ABC):
    def __init__(self, **kwargs: Any) -> None:
        pass
    
# --
# ...
# --
   
    instance: Any = None
    def __new__(cls, **kwargs: Any):
        
        if hasattr(cls, 'instance_args'):
            if cls.instance_args != kwargs:
                cls.instance = None
                
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)
            
            cls.instance_args = kwargs
            
            #create instance for loging
            cls.info = kwargs['log_info_class']
            cls.error = kwargs['log_error_class']
            
            cls.instance.config_dictionary = cls.get_config_dictionary()
                               
        return cls.instance
    
# --
# ...
# --
    
    @classmethod
    def get_config_dictionary(cls) -> str:
        return ''
        
# --
# ...
# --

    def __call__(self, **kwargs) -> str:
        return self.send_mail(**kwargs)