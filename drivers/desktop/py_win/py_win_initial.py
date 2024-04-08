from pywinauto.application import Application
from Setting.PyWin.mSetting import cSetting
from subprocess import Popen
from pywinauto import Desktop
import time

# --
# ...
# --

class PyWinInitial():
    def __init__(self, AppClass, ConnectionType='Application', Backend='uia', IsRunApp=False, IsUseHistory=False, IsVisible=False, IsWaitForVisible=True) -> None:
        self.session = None
        self.AppClass = AppClass
        self.ConnectionType = ConnectionType
        self.Backend = Backend
        self.IsRunApp = IsRunApp
        self.IsUseHistory = IsUseHistory
        self.IsVisible = IsVisible
        self.IsWaitForVisible = IsWaitForVisible
        self.SessionString = ''

        if self.ConnectionType == 'Application':
            self.session = Application(backend=self.Backend)
        else:
            self.IsRunApp = False
            Popen(self.AppClass.execFilename, shell=True)
            self.session = Desktop(backend=self.Backend)

# --
# ...
# --

    def InitialSession(self) -> None:
        SessionString = ''
        
        if self.IsRunApp:
            self.session.start(self.AppClass.path)
        else:
            self.session = self.session.connect(
                title=self.AppClass.title,
                timeout=cSetting.CreateSessionTimeout('s'),
                visible_only=self.IsVisible)

        time.sleep(cSetting.WitForAppLaunch('s'))
        self.SessionString = "self.session.window(title='" + str(self.AppClass.title) + "')"

        if self.IsWaitForVisible:
            SessionString = self.SessionString + ".wait('visible')"
            
        eval(SessionString)

# --
# ...
# --

    def TerminateSession(self):
        self.session = None

# --
# ...
# --

if __name__ == '__main__':
    pass
