from services.disk.xml.xml_manager import XMLManager

class DiskProvider:
    def __init__(self) -> None:
        self.xml_manager_class = XMLManager().instance