from abc import ABC, abstractmethod
 
class BaseTestComplete(ABC):
 
        @abstractmethod
        def WaitForAvailablity(cls):
                pass
#--
#...
#--            
        @abstractmethod
        def WaitForAvailablityWriter(cls):
                pass
#--
#...
#--             
        @abstractmethod                
        def WaitForNow(cls):
                pass
#--
#...
#--             
        @abstractmethod                
        def GetTodayDatum(cls):
                pass                       
#--
#...
#-- 
        @abstractmethod  
        def WaitForInt(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def GetTabPageIsVefugbar(cls):
                pass                                                
#--
#...
#-- 
        @abstractmethod 
        def SelectComboboxItem(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def SelectListBoxItem(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def SelectBarItem(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def SelectContextMenueBarItem(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def SelectContextMenueStrip(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def StateCheckBoxInTreeView(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def SelectCheckBoxInTableView(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def SelectComboboxItemInTableView(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def SelectDateTimeInTableView(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def SetTextInTableView(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def SetTextInListView(cls):
            pass
#--
#...
#-- 
        @abstractmethod 
        def ClickItemComboboxInListView(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def ClickButton(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def SelectButtonPopupItem(cls):
                pass   
#--
#...
#-- 
        @abstractmethod 
        def StateCheckBox(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def ClickItem(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def DblClickItem(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def CheckItem(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def SetText(cls):
                pass
    
#--
#...
#-- 
        @abstractmethod 
        def SetDate(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def ClickTab(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def Click(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def ClickR(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def Close(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def DblClick(cls):
                pass
#--
#...
#-- 
        @abstractmethod 
        def TreeViewClick(cls):
                pass
#--
#...
#--
        @abstractmethod  
        def ItemCount(cls):
            pass
#--
#...
#--        
        @abstractmethod 
        def ClickImage(cls):
                pass