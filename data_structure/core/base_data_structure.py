from typing import Any
from abc import ABC, abstractmethod


# --
# ...
# --
    
class BaseDataStructure(ABC):
    def __init__(self, **kwargs: Any) -> None:
        pass
    
# --
# ...
# --
   
    instance: Any = None
    def __new__(cls, *args, **kwargs: Any):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)

        return cls.instance
    
# --
# ...
# --

    def __call__(self) -> str:
        return self.instance
