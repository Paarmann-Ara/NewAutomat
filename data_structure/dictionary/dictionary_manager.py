from typing import Any
from data_structure.core.base_data_structure import BaseDataStructure

# --
# ...
# --


class DictionaryManager(BaseDataStructure):
    def __init__(self) -> None:
        pass

# --
# ...
# --

    def compair(self, dictionary_0={}, dictionary_1={}) -> Any:

        try:

            added_key = {}
            removed_key = {}
            difference = {}
            commen = {}

            dictionary_0_Keys = set(dictionary_0.keys())
            dictionary_1_Keys = set(dictionary_1.keys())
            
            shared_keys = dictionary_0_Keys.intersection(dictionary_1_Keys)
            
            added_key = dictionary_0_Keys - dictionary_1_Keys
            
            removed_key = dictionary_1_Keys - dictionary_0_Keys
            
            difference = {key: (dictionary_0[key], dictionary_1[key]) for key in shared_keys if dictionary_0[key] != dictionary_1[key]}
            
            commen = set(key for key in shared_keys if dictionary_0[key] == dictionary_1[key])
            
            return added_key, removed_key, difference, commen

        except Exception as exp:
            print(str(exp))