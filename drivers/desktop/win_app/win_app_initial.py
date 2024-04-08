from WAWi.Core.Engin.Helper.mhwnd import chwnd
from appium import webdriver
from WAWi.Toolboxs.mTime import cTime
from Toolboxs.mProcess import cProcess
from Setting.WinDriver.mSetting import cSetting

# --
# ...
# --

class InitialDriver():
    def __init__(self) -> None:
        self.session = None
        self.AppClass = None

# --
# ...
# --

    def InitialWinAppDriver(self, AppClass):
        cProcess.run(AppClass.path)
        cTime.sleep(1)
# --
# ...
# --

    def InitialTestApp(self, AppClass):
        if cProcess.get_IsRunnigProcesByName(AppClass.execFilename):
            self.SetupDriver(appTopLevelWindow=chwnd.get_hwndsbyProcessid(
                cProcess.get_ProcessIdByName(AppClass.execFilename, False)))
        else:
            self.SetupDriver(app=AppClass.path)
# --
# ...
# --

    def SetupDriver(self, app='', appTopLevelWindow=''):

        if len(app) > 1:
            desired_caps = {
                'app': str(app),
                'platformName': 'windows',
                'createSessionTimeout': cSetting.CreateSessionTimeout,
                'waitForAppLaunch': cSetting.WitForAppLaunch
            }

            self.session = webdriver.Remote(
                command_executor='http://127.0.0.1:4723',
                desired_capabilities=desired_caps)

            return

        elif len(appTopLevelWindow) > 0:
            for hwnd in appTopLevelWindow:
                desired_caps = {
                    'appTopLevelWindow': str(hwnd),
                    'platformName': 'windows',
                    'createSessionTimeout': cSetting.CreateSessionTimeout,
                    'waitForAppLaunch': cSetting.WitForAppLaunch
                }

                try:

                    self.session = webdriver.Remote(
                        command_executor='http://127.0.0.1:4723',
                        desired_capabilities=desired_caps, direct_connection=True)

                    time.sleep(1)
                    return

                except Exception:
                    pass
# --
# ...
# --

    def TerminateSession(self):
        self.session.quit()


# --
# ...
# --
if __name__ == '__main__':
    pass
