from services.ftp.ftp_provider import FTPProvider

ftp = FTPProvider(domain='aqc').ftp
ftp.connect_to_ftp()
ftp.get_current_working_directory()
ftp.change_current_working_directory(current_working_directory="/AQCsDB")
ftp.get_current_working_directory_files()
ftp.download_file()
ftp.upload_file()