from services.disk.json.json_manager import JSONManager
from services.disk.xml.xml_manager import XMLManager
from services.log_.log_provider import LogProvider
from services.log_.stack_context_provider import StackContextProvider
from services.mail.mail_provider import MailProvider
from services.disk.disk_provider import DiskProvider
from jtl_wawi.testcase.testcase_sample_provider import TestcaseSampelProvider
from jtl_wawi.testcase.testcase_object_provider import TestcaseObjectProvider
from services.db.sqlserver.sqlserver_provider import SqlserverProvider

#--
#...
#--


class ServiceProvider:
    def __init__(self) -> None:
        self.json = JSONManager().instance
        self.xml = XMLManager().instance
        self.stack = StackContextProvider().stack
        
        self.info = LogProvider(template='Pipeline',config='Pipeline').info
        self.error = LogProvider(template='error',config='error').error
        self.tc_mo = MailProvider(body='Test_body', subject='Test_Subjekt').tc_mo_instance
        
        self.db_connection = SqlserverProvider().db_connection
        self.db_command_execute = SqlserverProvider().db_command_execute
        self.db_execute = SqlserverProvider().db_execute
        
        self.objects_context_menu = TestcaseObjectProvider('objects_context_menu').object_class
        self.Simple_CSV_AnhangDatei = TestcaseSampelProvider('Simple_CSV_AnhangDatei').full_adress        