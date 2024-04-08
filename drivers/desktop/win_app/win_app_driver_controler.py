from Drivers.WinApp.WinAppInitial import InitialDriver
from Toolboxs.mProcess import cProcess
from WAWi.Setting.Applications.WinAppDriver import WinAppDriver
from WAWi.Setting.Applications.JTL_WAWi import JTL_WAWi
import time

#--
#...
#--
class WinAppDriverControl():
        def __init__(self) -> None:
                self.Driver = InitialDriver()
                self.Initial()
#--
#...
#--
        def Terminate(self):
                self.Driver.TerminateSession()
                app.terminat(WinAppDriver.execFilename)
                #app.terminat(JTL_WAWi.execFilename)                
#--
#...
#--
        def Initial(self):
                app.terminat(WinAppDriver.execFilename)
                
                Temp = InitialDriver()
                Temp.InitialWinAppDriver(WinAppDriver)
                Temp.InitialTestApp(JTL_WAWi)
                self.Driver = Temp
#--
#...
#--
if __name__ == '__main__':
        WinAppDriverControl()