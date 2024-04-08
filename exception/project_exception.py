class ProjectException(Exception):
    def __init__(self, *args: object) -> None:
       super().__init__(*args)

# --
# ...
# --

    def RecoverWAWi(ModuleName=''):
        # import mBase
        import Objects_mException

        if Objects_mException.Absturz_btnSchlie_en.Exists:
            Objects_mException.Absturz_btnSchlie_en.ClickButton()

        # Recover Exceptions
        import Objects_WAWi
        if Objects_WAWi.WAWi_Login.Exists:
            return

        Delay(2000)
        Log.Message('WAWi Absturz')
        # mBase.cBase.TestResult('AQC of WAWi says: Ich absturz. WAWi wird neuegestarten. Position ' + ModuleName, TypeOfResultObject = 'Bug')

        import mWAWi
        Temp = mWAWi.cWAWi()
        Temp.RunWAWi()

        return True
    
    
    

    
    
    
    
# --
# ...
# --


class cCallBugReport(ProjectException):
    def __init__(self, message=' * I have Called BugReport * '):
        self.message = message
# --
# ...
# --

    def __str__(self):
        return self.message
# --
# ...
# --


class cReturn(ProjectException):
    def __init__(self, message=' * I cannot continue * '):
        self.message = message
# --
# ...
# --

    def __str__(self):
        return self.message
# --
# ...
# --


class cTestAgin(ProjectException):
    def __init__(self, message=' * There is someting missed, Please run me again * '):
        self.message = message
# --
# ...
# --

    def __str__(self):
        return self.message
# --
# ...
# --


class cEingabeIstFalsch(ProjectException):
    def __init__(self, message=' * Eingabe ist Falsch, Bitte Nochmal testen * '):
        self.message = message
# --
# ...
# --

    def __str__(self):
        return self.message
# --
# ...
# --


class cIFindNothing(ProjectException):
    def __init__(self, message=' * Ich find nix da * '):
        self.message = message
# --
# ...
# --


class cWaitForAvailablityMainForm(ProjectException):
    def __init__(self, message=' * Das Hauptformular wurde nicht sichtbar sein * '):
        self.message = message
# --
# ...
# --

    def __str__(self):
        return self.message
# --
# ...
# --


class cObjectIsDisabled(ProjectException):
    def __init__(self, message=' * Something is wrong, I cannot continue, the object is disabled * '):
        self.message = message
# --
# ...
# --

    def __str__(self):
        return self.message
# --
# ...
# --


class cObjectIsNotExist(ProjectException):
    def __init__(self, message=' * Something is wrong, I cannot continue, the object is not Exist * '):
        self.message = message
# --
# ...
# --

    def __str__(self):
        return self.message
# --
# ...
# --


class cSetup(ProjectException):
    def __init__(self, message=' * Control Unit:  Something is wrong * '):
        self.message = message
# --
# ...
# --


class cCheckPointSelector(ProjectException):
    def __init__(self, message=' * Check Point Selector Unit:  Something is wrong * '):
        self.message = message
# --
# ...
# --


class cAfterSetup(ProjectException):
    def __init__(self, message=' * Check Point Selector Unit:  Something is wrong * '):
        self.message = message
# --
# ...
# --


class cChangeCheckListAndAntwortOrUseCheckListExt(ProjectException):
    def __init__(self, message=' * Check Point Selector Unit:  Something is wrong * '):
        self.message = message
# --
# ...
# --

    def __str__(self):
        return self.message
# --
# ...
# --


def ExceptionsMessage():
    Delay(1000)
    if self.MessagboxManager(MessageToCheck="HTTP-Verbindung mit JTL-Shop OK!\n\n", MessageObject=self.MsgBox_2, IndexObject=2):
        # if Objects_mException.WAWiSimpleMessage.Window("Static", "HTTP-Verbindung mit JTL-Shop OK!\n\n", 2).Exists:
        return True
    else:
        return False
# --
# ...
# --


def EventControlWindow_OnUnexpectedWindow(Sender, Window, LogParams):

    try:

        if not Config.IsInExternalMode:
            WindowDetector(Sender=Sender, Window=Window, LogParams=LogParams)

    except Exception as exp:
        Log.Message('EventControlWindow_OnUnexpectedWindow: ' + str(exp))
# --
# ...
# --


def EventControlWindow_OnOverlappingWindow(Sender, Window, OverlappingWindow, LogParams):

    try:

        if not Config.IsInExternalMode:
            WindowDetector(Sender=Sender, Window=Window, LogParams=LogParams)

    except Exception as exp:
        Log.Message('EventControlWindow_OnOverlappingWindow: ' + str(exp))
# --
# ...
# --


def WindowDetector(ModuleName=' UnKnown', Sender=None, Window=None, LogParams=None):
    import mBase
    import Objects_mException
    Options.Run.Timeout = mBase.cBase.getTime()

    returnValue = False
    IsMayBugDialog = False

    ModuleName = ModuleName[1:]

    if Config.IsInExternalMode:
        return returnValue

    Delay(1500)

    arWindows = Aliases.JTL_WAWi.FindAllChildren("WndClass", "*", 1)

    if arWindows != None:

        if len(arWindows) > 0:
            for it in arWindows:
                if it.WndCaption == 'JTL-Wawi':
                    IsMayBugDialog = True
                    break
        if not IsMayBugDialog:
            return returnValue

    else:
        # Fehler Window
        if not ImageRepository.Error.Sign.Exists() and not ImageRepository.Error.Absturz.Exists() and not ImageRepository.Error.ProgressBar.Exists():
            return returnValue

    # Check Messagebox
    if Objects_mException.MsgBox_1.Exists or Objects_mException.MsgBox_2.Exists or Objects_mException.MsgBox_0.Exists:
        Temp = mBase.cBase()
        Temp.MessagboxManager()
        return returnValue

    # Bug Window
    elif Objects_mException.Absturz_btnSchlie_en.Exists:
        returnValue = RecoverWAWi(ModuleName)

    elif ImageRepository.Error.ProgressBar.Exists():
        returnValue = RecoverWAWi(ModuleName)

    elif Objects_mException.Msgbox_3.Exists:
        if Objects_mException.Message_ZuWenigArbeitsspeicher.Exists:
            import mWAWi
            Temp = mWAWi.cWAWi()
            Temp.ShutdownWAWi()

        elif Objects_mException.Msgbox_3_btn_FehlerEinsehen.Exists and not Objects_mException.Msgbox_3_btn_SendToBugReport_0.Exists:
            Objects_mException.Msgbox_3_btnOK_BugReport_0.ClickButton()
            Delay(1000)

        returnValue = SendToBugReport(ModuleName, True)

    elif Objects_mException.BugAuftreten_Form.Exists:
        returnValue = SendToBugReport(ModuleName)

    elif Objects_mException.BugFehlerprotokoll_Form.Exists:
        returnValue = BugFehlerprotokoll(ModuleName)

    return returnValue
# --
# ...
# --


def BugFehlerprotokoll(ModuleName):
    import mBase
    import Objects_mException
    Options.Run.Timeout = mBase.cBase.getTime()

    self.WaitForAvailablity(Objects_mException.BugFehlerprotokoll_btnOk)
    Objects_mException.BugFehlerprotokoll_btnOk.Click()

    Delay(mBase.cBase.getTime('SmallTime'))
    Log.Message('WAWi sollte Fehlerprotokoll in ' + ModuleName)
    mBase.cBase.TestResult(
        'AQC of WAWi says: Ich bekomme Fehler. WAWi sollte Fehlerprotokoll in ' + ModuleName, TypeOfResultObject='Bug')

    import mWAWi
    Temp = mWAWi.cWAWi()
    Temp.RunWAWi()

    return True
# --
# ...
# --


def SendToBugReport(ModuleName, IsMessage_3=False):
    import mBase
    import Objects_mException

    try:

        # Windows_Msg_Crash
        Windows_Msg_Crash = Aliases.Windows_Msg_Crash.Crashed
        Windows_Msg_Crash_btnProgrammSchliesen = Aliases.Windows_Msg_Crash.Crashed.JTL_WAWi.CtrlNotifySink.btnProgrammSchliesen

        Temp = mBase.cBase()

        Delay(500)

        if IsMessage_3:
            if Objects_mException.Msgbox_3_btn_SendToBugReport_0.Exists:
                if Objects_mException.Msgbox_3_btn_SendToBugReport_0.Enabled:
                    Objects_mException.Msgbox_3_btn_SendToBugReport_0.ClickButton()
                    Delay(500)
                else:
                    return RecoverWAWi(ModuleName)

                Delay(1500)

                if Objects_mException.Msgbox_3_btnOK_BugReport_0.Exists:
                    Objects_mException.Msgbox_3_btnOK_BugReport_0.ClickButton()

                elif Objects_mException.Msgbox_3_btn_BugAnsehen_0.Exists:
                    Objects_mException.Msgbox_3_btnOK_1.ClickButton()
            else:
                Temp.MessagboxManager()
                return False

        else:

            if Temp.WaitForAvailablity(Objects_mException.BugAuftreten_btnSend, MCounter=3):
                Delay(500)

                if Objects_mException.BugAuftreten_btnSend.Enabled:
                    Objects_mException.BugAuftreten_btnSend.Click()
                else:
                    if Objects_mException.BugAuftreten_btnOK.Exists:
                        Objects_mException.BugAuftreten_btnOK.ClickButton()
                Delay(500)

                if Objects_mException.BugAuftreten_btnOK.Exists:
                    Objects_mException.BugAuftreten_btnOK.ClickButton()

            elif Temp.MessagboxManager():
                return False

            elif Objects_mException.Msgbox_3_btn_SendToBugReport_0.Exists:
                if Objects_mException.Msgbox_3_btn_SendToBugReport_0.Enabled:
                    Objects_mException.Msgbox_3_btn_SendToBugReport_0.ClickButton()
                    Delay(500)
                else:
                    return RecoverWAWi(ModuleName)

                Delay(500)

                if Objects_mException.Msgbox_3_btnOK_BugReport_0.Exists:
                    Objects_mException.Msgbox_3_btnOK_BugReport_0.ClickButton()
                elif Objects_mException.Msgbox_3_btn_BugAnsehen_0.Exists:
                    Objects_mException.Msgbox_3_btnOK_1.ClickButton()

            else:
                Delay(500)
                return RecoverWAWi(ModuleName)

        Delay(500)

        if Temp.WaitForAvailablity(Objects_mException.Msgbox_3_btnZusatzinformationenSenden):
            Objects_mException.Msgbox_3_btnZusatzinformationenSenden.Click()
            Delay(500)
        else:
            return RecoverWAWi(ModuleName)

        Delay(500)

        if Temp.WaitForAvailablity(Objects_mException.AdditionalInformation_Form):
            Objects_mException.AdditionalInformation_Txt.Keys(
                "TestComplete Meldung!! Für mehr info rufe Mohammad an. Fehler Codes is " + ModuleName + "!" + StackOperation())
            Delay(500)
        else:
            return RecoverWAWi(ModuleName)

        Delay(500)

        if Temp.WaitForAvailablity(Objects_mException.AdditionalInformation_btnOK):
            Objects_mException.AdditionalInformation_btnOK.ClickButton()
            Delay(500)

        else:
            return RecoverWAWi(ModuleName)

        try:

            if ImageRepository.Error.ProgressBar.Exists():
                raise cCallBugReport()

            if Temp.WaitForAvailablity(Objects_mException.Msgbox_3_Progressbar_0, MCounter=10):
                while Objects_mException.Msgbox_3_Progressbar_0.WaitProperty("Visible", True, Temp.getTime('SmallTime')):
                    Delay(Temp.getTime('SmallTime'))
                    if ImageRepository.Error.ProgressBar.Exists() or Objects_mException.Absturz_btnSchlie_en.Exists:
                        return RecoverWAWi(ModuleName)
            else:
                if ImageRepository.Error.ProgressBar.Exists() or Objects_mException.Absturz_btnSchlie_en.Exists:
                    return RecoverWAWi(ModuleName)

        except Exception as exp:
            Log.Message('Oh lalala, I crashed' + str(exp))

        finally:

            Temp.MessagboxManager()
            Delay(3000)

            if not ImageRepository.Error.ProgressBar.Exists():
                while Objects_mException.Absturz_btnSchlie_en.Exists or Windows_Msg_Crash.Exists:
                    if Objects_mException.Absturz_btnSchlie_en.Exists:
                        Objects_mException.Absturz_btnSchlie_en.ClickButton()
                        return RecoverWAWi(ModuleName)

                    if Windows_Msg_Crash.Exists:
                        Windows_Msg_Crash_btnProgrammSchliesen.Click()
                        return RecoverWAWi(ModuleName)

                    Delay(2000)

            else:
                Delay(30000)
                if Objects_mException.Absturz_btnSchlie_en.Exists:
                    Objects_mException.Absturz_btnSchlie_en.ClickButton()
                    return RecoverWAWi(ModuleName)

                if Windows_Msg_Crash.Exists:
                    Windows_Msg_Crash_btnProgrammSchliesen.Click()
                    return RecoverWAWi(ModuleName)

                if not Temp.MessagboxManager():
                    return RecoverWAWi(ModuleName)

            mBase.cBase.TestResult(
                'AQC of WAWi says: I crashed. BugInfo discoverd. Position ' + ModuleName, TypeOfResultObject='Bug')

            Config.NumberOfBurReportMessageInDesktop += 1

            if Config.NumberOfBurReportMessageInDesktop > 0:
                RecoverWAWi()
                return True

            WindowDetector(ModuleName)

            return True

    except Exception as exp:
        Log.Message(
            'Oh lalala, Send Bug crashed!!! I recover die WAWi' + str(exp))
        RecoverWAWi(ModuleName)

# --
# ...
# --


