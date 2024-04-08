from typing import Any
from abc import ABC, abstractmethod


# --
# ...
# --
    
class BaseMailTemplate(ABC):
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
            
            body = cls.clear_body(**kwargs)
            cls.instance.template_object = {'template': cls.get_template(), 'mixed_html': cls.get_mixed_html_body(body), 'body' : body}
                   
        return cls.instance
    
# --
# ...
# --
    
    @classmethod
    def get_mixed_html_body(cls, body) -> str:
        return ''
    
# --
# ...
# --
    
    @classmethod
    def get_template(cls) -> str:
        return ''
    
# --
# ...
# --

    @classmethod
    def clear_body(cls, **kwargs) -> str:
        body = kwargs['body']
        body = body.replace("\n", "<br>\n")
        body = body.replace(" ", "&nbsp;")
        return body
    
# --
# ...
# --

    def __call__(self) -> str:
        return self.template