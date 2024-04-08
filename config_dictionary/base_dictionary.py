from typing import Any
from abc import ABC, abstractmethod
from config_dictionary.defualt_dictionary import DefaultDictionary

# --
# ...
# --

    
class BaseDictionary(ABC):
    def __init__(self, *args, **kwargs: Any) -> None:
        self.dictionary: dict
    
# --
# ...
# --
   
    instance: Any = None
    def __new__(cls,*args:Any, **kwargs: Any):
        
        if hasattr(cls, 'instance_args') or hasattr(cls, 'instance_kwargs'):
            if cls.instance_kwargs != kwargs or cls.instance_args != args :
                cls.instance = None
                
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)

            cls.instance_args = args
            cls.instance_kwargs = kwargs
              
            cls.instance.dictionary = cls.get_dictionary(*args, **kwargs)
            
        cls.instance.dictionary = DefaultDictionary(cls.instance.dictionary)
        
        return cls.instance
    
# --
# ...
# --
    
    @classmethod
    def get_dictionary(cls, *args, **kwargs) -> dict:
        return {}
    
# --
# ...
# --

    def __call__(self, key: str, value: str = '') -> str:

        if value:
            self.dictionary[key] = value
        return self.dictionary[key]
