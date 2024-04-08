import re
import traceback
from services.log_.core.base_log import BaseLog
from services.log_.config.log_config import LogConfig
from typing import Any

# --
# ...
# --


class StackContext(BaseLog):
    object_name = None
    no_show_moduls = None
    no_show_methods = None
    
    def __init__(self) -> None:
        StackContext.no_show_moduls = self.config_dictionary[__name__]["no_show_moduls"]
        StackContext.no_show_methods = self.config_dictionary[__name__]["no_show_methods"]
        
#--
#...
#--

    @classmethod
    def get_config_dictionary(cls):
            return LogConfig().instance.dictionary
        
# --
# ...
# --
  
    def __str__(cls) -> str:
        return cls.StackOperation()
        
# --
# ...
# --
    @classmethod
    def StackOperation(cls, object_name='')-> Any:

        try:
            
            cls.object_name = object_name

            Stack:Any = ''

            if cls.object_name != '':
                Stack = re.search(r"([(]).+([)])", cls.object_name)

            else:
                for line in traceback.format_stack()[3:]:
                    # Data = re.search("([aq:]+\w+).+([, line ]+\d+).+([, in ]+\w+)", line)
                    Data = re.search(r"([aq:]+\w+).+([, line ]+\d+)", line)

                    if Data:
                        Module = Data.group(1)[3:]
                        Line = Data.group(2)[1:]

                        if Module not in cls.no_show_moduls:
                            Data = re.search(r"(\b, in\b.\w+)", line)
                            Method = '0'

                            if Data:
                                Method = Data.group()[5:]

                                if Method not in cls.no_show_methods:
                                    Stack = Stack + ' > ' + Module + \
                                        '.' + Method + '(' + Line + ')'

            return Stack

        except Exception as exp:
            print(f"{__file__}--->{__name__} : + {str(exp)}")