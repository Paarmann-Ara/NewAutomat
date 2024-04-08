from typing import Any
from abc import ABC, abstractmethod


# --
# ...
# --
    
class BaseDB(ABC):
    def __init__(self, *args, **kwargs: Any) -> None:
        pass
    
# --
# ...
# --
   
    instance = None
    def __new__(cls, **kwargs: Any):
        
        if hasattr(cls, 'instanceArgs'):
            if cls.instanceArgs != kwargs:
                cls.instance = None
            
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)
            cls.instanceArgs = kwargs
            
            #create instance for loging
            cls.info = kwargs['log_info_class']
            cls.error = kwargs['log_error_class']
            
            connectionstring = cls.create_connection_string(**kwargs)
            cls.instance.connection = cls.get_connection(connectionstring)
                
        return cls.instance
    
# --
# ...
# --
    
    @classmethod
    def create_connection_string(cls, **kwargs) -> str:
        return ''
    
# --
# ...
# --
    
    @classmethod
    def get_connection(cls, connectionstring: str) -> Any:
        return ''
    
# --
# ...
# --

    def __call__(self):
        return self.connection
