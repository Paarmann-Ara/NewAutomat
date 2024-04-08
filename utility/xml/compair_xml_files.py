from services.service_provider import ServiceProvider
from data_structure.data_structure_provider import DataStructureProvider

# --
# ...
# --

class CompairXmlFile:
    def __init__(self) -> None:
        self.dictionary = DataStructureProvider().dictionary
        self.xml = ServiceProvider().xml

# --
# ...
# --

    def operation(self, xml_file_0, xml_file_1):

        file_0 = self.xml.operation(xml_file_0)
        file_1 = self.xml.operation(xml_file_1)

        added_key, removed_key, difference, commen = self.dictionary.compair(file_0, file_1)
        
        return str(added_key), str(removed_key), str(difference), str(commen)