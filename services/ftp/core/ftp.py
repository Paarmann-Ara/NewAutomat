from services.ftp.core.base_ftp import BaseFTP
from services.ftp.config.ftp_config import FTPConfig
import os
from typing import Any
from ftplib import FTP_TLS

# --
# ...
# --


class FTP(BaseFTP):
    def __init__(self, **kwargs) -> None:

        try:
            
            self.ftp = None
            
            self.current_working_directory = None

            self.temp_location_for_download = None
            self.file_to_download = None

            self.temp_location_for_upload = None
            self.file_to_upload = None

            self.server = None
            self.user = None
            self.password = None
            
            # set domain
            if 'domain' in kwargs:
                self.domain_dictionary = self.instance.config_dictionary[kwargs['domain']]
                self.server = self.domain_dictionary['server']
                self.user = self.domain_dictionary['user']
                self.password = self.domain_dictionary['password']

                self.aqc_db_address = self.domain_dictionary['aqc_db_address']
                self.mail_db_address = self.domain_dictionary['mail_db_address']

                self.temp_location_for_download = self.domain_dictionary['temp_location_for_download']
                self.file_to_download = self.domain_dictionary['file_to_download']

                self.temp_location_for_upload = self.domain_dictionary['temp_location_for_upload']
                self.file_to_upload = self.domain_dictionary['file_to_upload']

            if 'server' in kwargs:
                self.server = None
                
            if 'user' in kwargs:
                self.user = None
                
            if 'password' in kwargs:
                self.password = None
                
        except Exception as exp:
            self.error(f"{__file__}--->{__name__}: {str(exp)}")

# --
# ...
# --

    @classmethod
    def get_config_dictionary(cls):
        return FTPConfig().instance.dictionary

# --
# ...
# --

    def connect_to_ftp(self, **kwargs) -> str:

        try:

            self.ftp = FTP_TLS(self.server, timeout=70000)
            self.ftp.login(self.user, self.password)

            return self.ftp.welcome

        except Exception as exp:
            self.error(f"{__file__}--->{__name__}: {str(exp)}")
            return False

# --
# ...
# --

    def get_current_working_directory(self) -> str:

        try:

            self.ftp.set_pasv(True)
            return self.ftp.pwd()

        except Exception as exp:
            self.error(f"{__file__}--->{__name__}: {str(exp)}")
            return False

# --
# ...
# --

    def change_current_working_directory(self, **kwargs) -> str:

        try:

            self.ftp.set_pasv(True)

            if 'current_working_directory' in kwargs:
                self.ftp.cwd(kwargs['current_working_directory'])
                return self.ftp.dir()

            return False

        except Exception as exp:
            self.error(f"{__file__}--->{__name__}: {str(exp)}")
            return False
        
# --
# ...
# --

    def get_current_working_directory_files(self, **kwargs) -> list:

        try:

            self.ftp.set_pasv(True)

            if 'current_working_directory' in kwargs:
                self.ftp.cwd(kwargs['current_working_directory'])
                
            return list(self.ftp.mlsd())

        except Exception as exp:
            self.error(f"{__file__}--->{__name__}: {str(exp)}")
            return False

# --
# ...
# --

    def download_file(self, **kwargs) -> bool:

        try:

            if 'file_to_download' in kwargs:
                self.file_to_download = kwargs['file_to_download']
                
            if 'temp_location_for_download' in kwargs:
                self.temp_location_for_download = kwargs['temp_location_for_download']
                
            if self.file_to_download is None or self.temp_location_for_download is None:
                return False

            self.ftp.set_pasv(True)

            file_to_download_size = int(list(filter(lambda x: self.file_to_download in x, list(
                self.ftp.mlsd(facts=["size"]))))[0][1]['size'])

            file_to_download_size = file_to_download_size/(8 * 1024)

            with open(self.temp_location_for_download + '/' + self.file_to_download, 'wb') as writer:
                self.ftp.retrbinary(
                    f"RETR {self.file_to_download}",  writer.write, 8 * 1024)

                return True

        except Exception as exp:
            self.error(f"{__file__}--->{__name__}: {str(exp)}")
            return False

# --
# ...
# --

    def upload_file(self, **kwargs) -> bool:

        try:

            if 'file_to_upload' in kwargs:
                self.file_to_upload = kwargs['file_to_upload']
                
            if 'temp_location_for_upload' in kwargs:
                self.temp_location_for_upload = kwargs['temp_location_for_upload']
                
            if self.file_to_upload is None or self.temp_location_for_upload is None:
                return False

            self.ftp.set_pasv(True)

            with open(
                self.temp_location_for_upload + '/' + self.file_to_upload, 'rb') as reader:
                self.ftp.storbinary('STOR ' + self.file_to_upload, reader)

            return True

        except Exception as exp:
            self.error(f"{__file__}--->{__name__}: {str(exp)}")
            return False