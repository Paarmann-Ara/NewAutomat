from config_dictionary.base_dictionary import BaseDictionary
from services.disk.json.json_manager import JSONManager
import CONSTS

# --
# ...
# --

class DBConfig(BaseDictionary):
    @classmethod
    def get_dictionary(cls, *args) -> dict:
        json = JSONManager().instance
        config_json = json.operation(CONSTS.CONFIG_JSON)
        
        if __name__ in config_json:
            return config_json[__name__]
        
        else:
            return {}