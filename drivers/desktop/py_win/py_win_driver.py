from WAWi.Core.Control.PyWinControl import PyWinControl

# --
# ...
# --

class PyWin():
    def __init__(self, AppName, Parent='', Item='') -> None:
        self.Driver = PyWinControl(AppName).Driver
        self.session = self.Driver.session
        self.SessionString = self.Driver.SessionString
        
        self.Parent = self.Driver.AppClass.title  if Parent == '' else Parent
        self.Item = Item
        
# --
# ...
# --

    def Aktion(self, evalString, IsChangeSessioString):
        if IsChangeSessioString: self.SessionString = evalString
        eval(evalString)
        
# --
# ...
# --

    def getAllChild(self, IsChangeSessioString = False):
        evalString = self.SessionString + '.print_control_identifiers()'
        self.Aktion(evalString, IsChangeSessioString)

# --
# ...
# --

    def getForm(self, Form: str, IsChangeSessioString = False):
        evalString = self.SessionString + '.child_window(best_match="' + Form + '")'
        self.Aktion(evalString, IsChangeSessioString)
        
# --
# ...
# --

    def Click(self, Object: str, IsChangeSessioString = False):
        evalString = self.SessionString + '.child_window(best_match="' + Object + '").wrapper_object().click()'
        self.Aktion(evalString, IsChangeSessioString)

# --
# ...
# --

if __name__ == '__main__':
    pass

    