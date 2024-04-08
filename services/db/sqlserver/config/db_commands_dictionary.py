from config_dictionary.base_dictionary import BaseDictionary
from services.disk.json.json_manager import JSONManager
import CONSTS

# --
# ...
# --

class DBCommandsDictionary(BaseDictionary):
    @classmethod
    def get_dictionary(cls, **kwargs) -> dict:

        listview_name = kwargs.get('listview_name') if 'listview_name' in kwargs else ''
        node_name = kwargs.get('node_name') if 'node_name' in kwargs else ''
        column_name = kwargs.get('column_name') if 'column_name' in kwargs else ''
        time_metric = kwargs.get('time_metric') if 'time_metric' in kwargs else ''
        log_info = kwargs.get('log_info') if 'log_info' in kwargs else ''
        
        testme_db_folder = kwargs.get('testme_db_folder') if 'testme_db_folder' in kwargs else ''
        testme_db = kwargs.get('testme_db') if 'testme_db' in kwargs else ''
        testme_version_folder = kwargs.get('testme_version_folder') if 'testme_version_folder' in kwargs else ''
        
        json = JSONManager().instance
        config_json_dictionary = json.operation(CONSTS.CONFIG_JSON)[__name__]
        
        default_db_name = config_json_dictionary['default_db_name']
        default_backup_adress = config_json_dictionary['default_backup_adress']
        default_db_data_name = config_json_dictionary['default_db_data_name']
        default_db_data_adress = config_json_dictionary['default_db_data_adress']
        default_db_log_name = config_json_dictionary['default_db_log_name']
        default_db_log_adress = config_json_dictionary['default_db_log_adress']
        
        dictionary = {
            'STANDARD': f""" USE MASTER;SELECT DATABASEPROPERTYEX ('eazybusiness', 'STATUS') """,
            'AC': f""" USE MASTER;SELECT user_access FROM sys.databases WHERE name = 'eazybusiness' """,
            'MU': f""" USE MASTER;DECLARE @kill varchar(8000) = ''; SELECT @kill = @kill + 'kill' + CONVERT(varchar(5), session_id) + \';\' FROM sys.dm_exec_sessions WHERE database_id  = db_id(\'eazybusiness\') EXEC(@kill);ALTER DATABASE eazybusiness SET MULTI_USER """,
            'Del': f""" USE AQC;TRUNCATE TABLE ListViewCheck """,
            'LogTime': f"""USE AQC;INSERT INTO [ListViewCheck] ([ListViewName], [Node], [Spalte], [Time], [Loginfo]) VALUES ('{listview_name}', '{node_name}', '{column_name}', '{time_metric}', '{log_info}') """,
            'DB_Restore': f""" USE MASTER;ALTER DATABASE {default_db_name} SET SINGLE_USER WITH ROLLBACK IMMEDIATE; RESTORE DATABASE {default_db_name} FROM DISK = '{default_backup_adress}' WITH MOVE '{default_db_data_name}' TO '{default_db_data_adress}', MOVE '{default_db_log_name}' TO '{default_db_log_adress}', REPLACE, RECOVERY, STATS = 10;ALTER DATABASE {default_db_name} SET MULTI_USER """,
            'DB_MailRestore': f""" USE MASTER;ALTER DATABASE {default_db_name} SET SINGLE_USER WITH ROLLBACK IMMEDIATE; RESTORE DATABASE {default_db_name} FROM DISK = 'C:\Mad-Grb\Apps\DB.BAK' WITH MOVE '{default_db_data_name}' TO '{default_db_data_adress}', MOVE '{default_db_log_name}' TO '{default_db_log_adress}', REPLACE, RECOVERY, STATS = 10;ALTER DATABASE {default_db_name} SET MULTI_USER """,
            'DB_TestMeRestore': f""" USE MASTER;ALTER DATABASE {default_db_name} SET SINGLE_USER WITH ROLLBACK IMMEDIATE;RESTORE DATABASE {default_db_name} FROM DISK = '{testme_db_folder}\{testme_db}' WITH MOVE '{default_db_data_name}' TO '{default_db_data_adress}', MOVE '{default_db_log_name}' TO '{default_db_log_adress}', REPLACE, RECOVERY, NOUNLOAD;ALTER DATABASE {default_db_name} SET MULTI_USER """,
            'DB_TestMeBackup': f""" USE MASTER;ALTER DATABASE {default_db_name} SET SINGLE_USER WITH ROLLBACK IMMEDIATE; BACKUP DATABASE {default_db_name} TO DISK = '{testme_version_folder}/DB.bak' WITH STATS = 10;ALTER DATABASE {default_db_name} SET MULTI_USER """,
            'Error': f""" USE AQC;INSERT INTO [Errors] ([Loginfo]) VALUES ('{log_info}') """,
        }
        
        return dictionary
        