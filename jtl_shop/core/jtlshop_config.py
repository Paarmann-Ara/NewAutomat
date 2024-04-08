from config_dictionary.base_dictionary import BaseDictionary
from services.disk.json.json_manager import JSONManager

# --
# ...
# --

class JtlShopConfig(BaseDictionary):
    @classmethod
    def get_dictionary(cls, args) -> dict:
        json = JSONManager().instance
        return json.operation(args)