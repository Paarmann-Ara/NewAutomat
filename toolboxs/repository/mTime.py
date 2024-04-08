from Toolboxs.Repository.Base.mBaseDictionary import BaseDictionary
from Toolboxs.Repository.mTimeDictionary import cTimeDictionary


# --
# ...
# --

class cTime(BaseDictionary):
        @classmethod
        def get_dictionary(cls):
                return cTimeDictionary()()