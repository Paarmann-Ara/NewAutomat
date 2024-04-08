from Toolboxs.mProcess import cProcess
from Drivers.PyWin.PyWinInitial import PyWinInitial
from WAWi.Setting.Applications.AppClass import AppClass

# --
# ...
# --

class PyWinControl():
    def __init__(self, AppName) -> None:
        self.AppClass=AppClass(AppName).Value
        self.Driver = PyWinInitial(self.AppClass)
        self.Initial()
        
# --
# ...
# --

    def Terminate(self):
        cProcess.terminat(self.AppClass)
    
# --
# ...
# --

    def Initial(self):
        self.Driver.InitialSession()

# --
# ...
# --

if __name__ == '__main__':
    pass
