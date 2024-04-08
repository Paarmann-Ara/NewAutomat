from services.disk.core.base_disk import BaseDisk

# --
# ...
# --


class FileManager(BaseDisk):
    def __init__(self) -> None:
        pass

# --
# ...
# --

    def operation(self, mode='a', adress='', context='')-> str:
        
        try:
            
            with open(adress, mode) as file:
                if context:
                    file.write(context)
                    
                else:
                    context = file.read()
                    
            file.close()
        
        except Exception as exp:
            print(str(exp))
            context = 'Error'
            
        finally:
            return context
        