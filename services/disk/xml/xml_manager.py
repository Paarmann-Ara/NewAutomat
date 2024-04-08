from services.disk.core.base_disk import BaseDisk
from xml.dom import minidom
from typing import Any
import xmltodict
from io import BytesIO
from dict2xml import dict2xml

# --
# ...
# --


class XMLManager(BaseDisk):
    def __init__(self) -> None:
        pass

# --
# ...
# --

    def operation(self, adress='', context='', is_get_string = False, is_get_dictionary = True) -> Any:
        
        try:
            xml_data = None
            
            if (context == ''):
               with open(adress, 'r') as file:
                    readed_file = file.read()
                    corrected_file_string = self.__fix_xml_error(readed_file)
                    xml_data = minidom.parseString(corrected_file_string)
                                        
                    if is_get_string:
                        xml_data = corrected_file_string
                        
                    if is_get_dictionary:
                        from io import BytesIO
                        xml_data = xmltodict.parse(BytesIO(bytes(corrected_file_string,encoding='utf-8')))
                        
            else:
                with open(adress, 'w') as file:
                    corrected_file_string = self.__fix_xml_error(context)
                    xml_data_string = dict2xml(corrected_file_string)
                    file.write(xml_data_string)
                    xml_data = True
                    
            return xml_data
        
        except Exception as exp:
            print(str(exp))
            
# --
# ...
# --

    def __fix_xml_error(self, context='')-> str:
        
        try:

            ...
                                
        except Exception as exp:
            print(str(exp))
            context = 'Error'
            
        finally:
            return context
        