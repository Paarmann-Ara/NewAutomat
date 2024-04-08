from typing import Any
from abc import ABC, abstractmethod


# --
# ...
# --

class DefaultDictionary(dict):
    def __missing__(self, key):
        return 'nothing'

# --
# ...
# --
    
class BaseDictionary(ABC):
    def __init__(self) -> None:
        pass
    
# --
# ...
# --
   
    instance = None
    def __new__(cls, **kwargs: Any):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls, **kwargs)
            
            cls.instance.dictionary = cls.get_dictionary()
            
        cls.instance.dictionary = DefaultDictionary(
            cls.instance.dictionary)
        
        return cls.instance
    
# --
# ...
# --
    
    @classmethod
    def get_dictionary(cls) -> dict:
        return {}
    
# --
# ...
# --

    def __call__(self, Key: str, Value: str = '') -> str:

        if Value:
            self.dictionary[key] = Value

        print(id(self))
        return self.dictionary[key]
