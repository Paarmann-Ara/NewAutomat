from enum import Enum
from toolboxs.toolbox import Toolbox

ROOT_DIR = Toolbox.get_root_path()

CONFIG_JSON = ROOT_DIR + '/config_dictionary/config.json'
TESTCASE_DIR = ROOT_DIR + '/wawi/testcase/testcase_object'

class JTLSHOPCONFIG(Enum):
    OBJECT_JSON = ROOT_DIR + '/jtl_shop/testcase/objects/'