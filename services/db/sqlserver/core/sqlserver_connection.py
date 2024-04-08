from typing import Any
from services.db.sqlserver.core.base_db import BaseDB
import pyodbc

#--
#...
#--


class SqlserverConnection(BaseDB):
    
#--
#...
#--

    @classmethod
    def create_connection_string(cls, **kwargs) -> str:
        
        try:
            
            return f"""DRIVER={{{kwargs['driver']}}};server={kwargs['host']};database={kwargs['database']};trusted_connection=yes;uid={kwargs['username']};pwd={kwargs['password']};"""
        
        except Exception as exp:
            cls.error(f"{__file__}--->{__name__}: {str(exp)}")

#--
#...
#--

    @classmethod
    def get_connection(cls, connection_string: str) -> Any:
        
        try:
            
            return pyodbc.connect(connection_string, autocommit=True)
        
        except Exception as exp:
            cls.error(f"{__file__}--->{__name__}: {str(exp)}")