from services.disk.core.base_disk import BaseDisk
import json
from typing import Any

# --
# ...
# --


class JSONManager(BaseDisk):
    def __init__(self) -> None:
        pass

# --
# ...
# --

    def operation(self, adress='', context='', is_get_dictionary = True) -> Any:
        
        try:
            json_data = None
            
            if (context == ''):
               with open(adress, 'r') as file:
                    readed_file = file.read()
                    corrected_file_string = self.__fix_json_error(readed_file)
                    json_data = json.loads(corrected_file_string)
                    
                    if is_get_dictionary:
                        json_data = dict(json_data)
                    
            else:
                with open(adress, 'w') as file:
                    corrected_file_string = self.__fix_json_error(context)
                    json.dumps(corrected_file_string, indent=4)
                    file.write(corrected_file_string)
                    json_data = True
                    
            return json_data
        
        except Exception as exp:
            print(str(exp))
# --
# ...
# --

    def __fix_json_error(self, context='')-> str:
        
        try:

            context = context.replace(chr(92), chr(47))
            context = context.replace(chr(39), chr(34))
            
            return context
                    
        except Exception as exp:
            print(str(exp))