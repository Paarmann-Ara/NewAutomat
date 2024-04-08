class PyWinTools():

    #false name
    @staticmethod
    def getWinTitle(AppClass):
        Expr = ''
        WinTitle = AppClass
        myVars = locals()
        myVars.__setitem__(WinTitle, AppClass)

        eval('self.session.' + self.Driver.AppClass.WindowTitle +
             '.print_control_identifiers()')
