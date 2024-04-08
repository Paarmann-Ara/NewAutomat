from services.log_.core.loging.log import Log
from services.disk.file.file_manager import FileManager

# --
# ...
# --


class LogProvider:
    def __init__(self, template='Pipeline', config='Pipeline') -> None:
        
        self.file_manager_class = FileManager().instance
        
        self.info = Log(template=template, config=config, file_manager_class=self.file_manager_class).instance.info
        self.error = Log(template='Error', config='Error', file_manager_class=self.file_manager_class).instance.error