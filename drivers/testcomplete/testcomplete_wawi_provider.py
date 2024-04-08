from services.log_.log_provider import LogProvider
from services.log_.stack_context_provider import StackContextProvider
from jtl_wawi.testcase.testcase_object_provider import TestcaseObjectProvider
from drivers.testcomplete.core.testcomplete_driver import TestCompleteDriver
from drivers.testcomplete.config.testcomplete_config import TestcompleteConfig

#--
#...
#--


class TestcompleteWawiProvider():
    def __init__(self) -> None:
        
        # provide log objects
        log_info_class = LogProvider().info
        log_error_class = LogProvider().error
        stack = StackContextProvider().stack

        # provide config dictionary
        driver_config_dictionary = TestcompleteConfig().instance.dictionary
        
        # provide testcase_object
        objects_context_menu = TestcaseObjectProvider('objects_context_menu').object_class
        
        # testcomplete_driver object
        self.testcomplete_driver = TestCompleteDriver(objects_context_menu=objects_context_menu, driver_config_dictionary=driver_config_dictionary, log_info_class=log_info_class, log_error_class=log_error_class, stack=stack).instance



