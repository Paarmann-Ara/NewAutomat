from services.log_.log_provider import LogProvider
from services.db.sqlserver.config.db_config import DBConfig
from services.db.sqlserver.core.sqlserver_connection import SqlserverConnection
from services.db.sqlserver.core.sqlserver_execute import SqlserverExecute
from services.db.sqlserver.config.db_commands_dictionary import DBCommandsDictionary

#--
#...
#--


class SqlserverProvider:
    def __init__(self, driver='', host='', database='', username='', password='', db_command = 'DB_TestMeRestore', command = '', is_use_default = True, **kwargs) -> None:
        #create log
        self.log_info_class = LogProvider().info
        self.log_error_class = LogProvider().error
        
        # create config dictionary
        if is_use_default:
            db_config_dictionary = DBConfig().instance.dictionary
            driver = db_config_dictionary['driver']
            host = db_config_dictionary['host'].replace('/','\\')
            database = db_config_dictionary['database']
            username = db_config_dictionary['username']
            password = db_config_dictionary['password']        

            if db_command:
                testme_db_folder = db_config_dictionary['testme_db_folder']
                testme_db = db_config_dictionary['testme_db']
                
        if db_command: 
            db_command = DBCommandsDictionary(testme_db_folder=testme_db_folder, testme_db=testme_db, **kwargs).instance.dictionary[db_command]
        
        self.db_connection = SqlserverConnection(driver=driver, host=host, database=database, username=username, password=password, log_info_class=self.log_info_class, log_error_class=self.log_error_class, **kwargs).instance.connection
        self.db_command_execute = SqlserverExecute(sqlserver_connection=self.db_connection, db_command=db_command, command=command, log_info_class=self.log_info_class, log_error_class=self.log_error_class, **kwargs).execute_db_command
        self.db_execute = SqlserverExecute(sqlserver_connection=self.db_connection, db_command=db_command, command=command, log_info_class=self.log_info_class, log_error_class=self.log_error_class, **kwargs).execute_command