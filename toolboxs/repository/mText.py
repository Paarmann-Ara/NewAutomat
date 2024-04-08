from Toolboxs.Repository.Base.mBaseDictionary import BaseDictionary
from Toolboxs.Repository.mTextDictionary import cTextDictionary


# --
# ...
# --

class cText(BaseDictionary):
        @classmethod
        def get_dictionary(cls):
                return cTextDictionary()()