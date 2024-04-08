from services.ftp.core.ftp import FTP
from services.log_.log_provider import LogProvider


class FTPProvider:
    def __init__(self, domain='aqc', current_working_directory=None, file_to_download=None, temp_location_for_download=None, **kwargs) -> None:
        self.log_info_class = LogProvider().info
        self.log_error_class = LogProvider().error
        
        self.ftp = FTP(domain=domain, log_info_class=self.log_info_class, log_error_class=self.log_error_class, **kwargs).instance