from data_structure.dictionary.dictionary_manager import DictionaryManager

class DataStructureProvider:
    def __init__(self, **kwargs) -> None:
        self.dictionary = DictionaryManager(**kwargs).instance
        