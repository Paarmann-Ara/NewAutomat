from services.db.sqlserver.sqlserver_provider import SqlserverProvider

db_command_execute = SqlserverProvider(db_command = 'DB_TestMeRestore').db_command_execute
db_command_execute()

db_execute = SqlserverProvider(command = 'USE eazybusiness;SET NOCOUNT ON; SELECT * FROM dbo.tRMGrund').db_execute
print(db_execute())