from drivers.testcomplete.core.base_testcomplete import BaseTestComplete
import datetime
import math
from exception.project_exception import ProjectException
import types
from drivers.testcomplete.core.testcomplete_tools import TestCompleteTools
from toolboxs.delay import Delay

#--
#...
#--


class TestCompleteDriver(BaseTestComplete):
      
#--
#...
#--
  
    def __init__(self, **kwargs):
        self.temp_objects_log = []
        
        self.objects_context_menu = kwargs['objects_context_menu']
        self.driver_config_dictionary = kwargs['driver_config_dictionary']
        
        
        self.object_s_context_menu = object_s_context_menu
        

#--
#...
#--
        
    def wait_for_availability(self, object_, object_name = " Nothing ", counter = 10, just_exists = False, is_report = True, method = 'Unkown'):
            Delay(0.01)
                
            is_existing = False
    
            stack = '0'
            stack = StackContext(object_)
            
            if object_ is None or object_ == 'nothing' or type(object_) == str:
                    object_ = None
                    self.log_info.Info(f" * AQC of WAWi says: I am waiting for {object_name} but find nothing *>>> {stack}")
                    self.wait_for_availability_writer(object_, 'False', is_report, is_existing, method, stack = stack)
                    return False
    
            if not hasattr(object_, 'Enabled') and not just_exists:    
                    object_ = None 
                    self.log_info.Info(f" * AQC of WAWi says: I am waiting for {object_name} but find nothing *>>>  {stack}")
                    self.wait_for_availability_writer(object_, 'False', is_report, is_existing, method, stack = stack) 
                    return False
        
            Counter = 0 
    
            if hasattr(object_, 'Exists'):
                    while True:
                            if object_.Exists:
                                    is_existing = True
                                    break
                            if Counter > counter :
                                    is_existing = False
                                    break
                            Delay(250)
                            Counter += 1
                
                                    
            if is_existing:
                    if hasattr(object_, 'Visible') and not just_exists:
                            while not object_.Visible:
                                    Counter += 1
                                    Delay(250)
                                    
                                    if Counter > counter:
                                            object_ = None
                                            Counter = None
                                            self.log_info.Info(f" * AQC of WAWi says: I am waiting for {object_name} but find nothing *>>>{stack}") 
                                            self.wait_for_availability_writer(object_, 'False', is_report, is_existing, method, stack = stack)
                                            return False
                                    
              
                    Counter = 0                                        
    
                    if not just_exists:
                            while not object_.Enabled:
                                    Counter += 1
                                    Delay(250)
                                    if Counter > counter / 10:        
                                            if not object_.Enabled:
                                                    object_ = None
                                                    Counter = None
                                                    self.log_info.Info(f" * AQC of WAWi says: I am waiting for {object_name} but find nothing *>>> {stack}") 
                                                    self.wait_for_availability_writer(object_, 'False', is_report, is_existing, method, stack = stack)
                                                    return False

                    self.wait_for_availability_writer(object_, 'True', is_report, is_existing, method, stack = stack)
                    object_ = None
                    Counter = None
                    return True
            else:   
                    self.wait_for_availability_writer(object_, 'False', is_report, is_existing, method, stack = stack)             
                    object_ = None
                    Counter = None
                    return False      
#--
#...
#--            
    
    def wait_for_availability_writer(self, object_, result, is_report, is_existing, method, stack):
        
            try:
        
                    mode = 'Config.Testmode'
                    
                    if not is_report:
                            return
                            
                    if object_ == None:
                            return
                    
                    if not hasattr(object_, 'MappedName'):
                            return

                    zeichnen = 3*' '
                    
                    if mode == 'Standard':
                            mode = '   STD   '
                            
                    elif mode == 'Test':
                            mode = '   TST   '
                            
                    else:
                            mode = '   ???   '
                                                           
                    if result == 'False':
                            result = '[!]'
                            zeichnen = 2*' '
                            mode = mode[1:]
                            
                    else:
                            result = 'T'
                            
                    if is_existing:
                            e_flag = '+'
                    else:
                            e_flag = '-'
                            
                    is_existing = ' (' + e_flag + ') '
                    
                    method = ''
                    
                    self.temp_objects_log.append(str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")) + zeichnen + result + is_existing + mode + method.ljust(75, ' ')  + object_.MappedName.ljust(400, ' ') + stack + ' \n')
            
                    self.log_info.Info(result + zeichnen + object_.MappedName + ' -> ' + method + ' >>> ' + stack)
                    
                    Delay(50)
                    
                    # if len(self.temp_objects_log) > Config.QTYofself.temp_objects_logInBatch:
                    #         result = '\n'
                    #         for it in self.temp_objects_log:
                    #                 result = result + it
                    #         self.temp_objects_log.clear()
                            
                    #         TempFile = open(Config.self.temp_objects_log, 'a')
                    #         TempFile.write(result)
                    #         TempFile.close()   
                             
                    #         Delay(Config.QTYofself.temp_objects_logInBatch * 10)

            except Exception as exp:
                    self.log_info.Info('wait_for_availability_writer' + str(exp))
                    
                    
                    
# #--
# #...
# #--             
#     @staticmethod                
#     def WaitForNow():
        
#             try:
            
#                     Counter = 0
#                     NOW = datetime.datetime.now()
#                     while True:
#                             if isinstance(NOW, datetime.datetime):
#                                     break
#                     return NOW

#             except Exception as exp:
#                     self.log_info.Info('WaitForNow:' + str(exp)) 
# #--
# #...
# #--             
#     @staticmethod                
#     def GetTodayDatum():
        
#             try:
            
#                     return date.today()

#             except Exception as exp:
#                     self.log_info.Info('GetTodayDatum' + str(exp))                         
# #--
# #...
# #-- 
#     @staticmethod  
#     def WaitForInt(object_, Message = ""):
        
#             try:
            
#                     Delay(150)
#                     NumberTypes = (types.IntType, types.LongType, types.FloatType, types.ComplexType)

#                     if object_ is None or object_ == 'nothing' or not isinstance(object_, NumberTypes): # or isinstance(object_, 'IDispatchWrapper_AnyUsageStub'):
#                             object_ = None
#                             return 0
                    
#                     Number = object_
                    
#                     while True:
#                             if isinstance(Number, int):
#                                     break
#                             Delay(150)
#                             Number = object_
                            
#                     object_ = None
                    
#                     return Number           

#             except Exception as exp:
#                     self.log_info.Info('WaitForInt: ' + str(exp))
# #--
# #...
# #-- 
#     def GetTabPageIsVefugbar(self, Tabobject_, TabName = '',TabNummer = 0):
#             Options.Run.Timeout = 250
            
#             try:
            
#                     self.wait_for_availability(Tabobject_, method = 'GetTabPageIsVefugbar->' + str(TabName))
#                     ItemIndex = 0
    
#                     if not hasattr(Tabobject_, 'TabCount') or not hasattr(Tabobject_, 'tabCollection'):
#                             return False
            
#                     if TabNummer == 0:
#                             for ItemIndex in range (0,Tabobject_.TabCount, 1):
#                                     if TabName == Tabobject_.tabCollection.Item[ItemIndex].Text.OleValue:
#                                             return True
#                     elif TabNummer != 0:
#                             if Tabobject_.TabCount > TabNummer:
#                                     return True
#                     return False   
            
#             except Exception as exp:
#                     self.log_info.Info('GetTabPageIsVefugbar:' + str(exp))                                                     
# #--
# #...
# #-- 
#     def SelectComboboxItem(self, Combobox, Contain = '', IsRaiseException = False, WaitDelay = 50):

#             try:

#                     Index = 1
#                     ZielContent = ''
                    
#                     if not self.wait_for_availability(Combobox, counter = 3, method = 'SelectComboboxItem->' + str(Contain)):
#                             raise ProjectException.cobject_IsNotExist()  
                    
#                     if not Combobox.Visible:
#                             raise ProjectException.cobject_IsNotExist()
                    
#                     if not Combobox.Exists:
#                             raise ProjectException.cobject_IsNotExist()
                    
#                     if not Combobox.Enabled:
#                             self.Testresult('Combobox ' + Combobox.Name + ' :', TypeOfresultobject_ = 'object_s') 
#                             raise ProjectException.cobject_IsDisabled()
                                            
#                     if hasattr(Combobox, 'DropDown'):
#                             Combobox.DropDown()
#                     else:
#                             Combobox.Click()
                    
#                     Delay(WaitDelay)
                           
#                     Item = Aliases.JTL_WAWi.Popup.Root.PopupContentControl
                    
#                     Delay(WaitDelay)
                    
#                     if not Item.Exists or Item == None :
#                             Item = Combobox.PopupElement
#                             Delay(WaitDelay)
            
#                     SubItem = Item.FindChildEx('WPFControlText',Contain,5)
                    
#                     if not SubItem.Exists and Item.ChildCount > 0 and not isinstance(Contain, int):
#                             for Index in range(Item.ChildCount):
                            
#                                     try:
                                    
#                                             ZielItem = Item.WPFobject_("ComboBoxEditItem", '', Index)
                                            
#                                     except Exception as exp:
#                                             pass
                            
#                                     Delay(WaitDelay)
                                    
#                                     if ZielItem.Exists:
#                                             if hasattr(ZielItem.Content, 'Name'):
#                                                     ZielContent = ZielItem.Content.Name.OleValue
                                                    
#                                             elif hasattr(ZielItem.DataContext, 'DisplayMember'):
#                                                     ZielContent = ZielItem.DataContext.DisplayMember.OleValue
                                            
#                                             if ZielContent == Contain:
#                                                     SubItem = Item.WPFobject_('ComboBoxEditItem', '',Index)
#                                                     break
                    
#                     Delay(WaitDelay)
            
#                     if isinstance(Contain, int):
#                             if Contain == 0 :
#                                     Contain = 1
                            
#                             Item.WPFobject_("ComboBoxEditItem", '', Contain).Click()
#                     elif Contain == '':
#                             Item.WPFobject_("ComboBoxEditItem", Contain,1).Click()
#                     else:
#                             if SubItem.Exists:
#                                     SubItem.DblClick()
#                             else:
#                                     Item.WPFobject_("ComboBoxEditItem", '', 1).Click()
            
#                     Delay(WaitDelay) 
            
#                     if hasattr(Combobox, 'CloseUp'):
#                             Combobox.CloseUp()   
#                     else:
#                             Combobox.Click()
            
#             except Exception as exp:
#                     self.log_info.Info('SelectComboboxItem - type:' + str(exp))
#                     if Combobox != None and hasattr(Combobox, 'Name'):
#                             self.Testresult('SelectComboboxItem '  + Combobox.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('SelectComboboxItem: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))        
#                     if IsRaiseException:
#                               raise ProjectException.cReturn()
#                     else:
#                             return False                        
# #--
# #...
# #-- 
#     def SelectListBoxItem(self, ListBox, Contain = ''):

#             try:
    
#                     self.wait_for_availability(ListBox, method = 'SelectListBoxItem->' + str(Contain))
            
#                     ListBox.Click()
            
#                     Item = Aliases.JTL_WAWi.Popup.Root.ListBoxEdit
            
#                     self.wait_for_availability(Item, method = 'SelectListBoxItem->' + str(Contain))
            
#                     SubItem = Item.FindChild('WPFControlText',Contain,5)
            
#                     if isinstance(Contain, int):
#                             if Contain == 0 :
#                                     Contain = 1
                            
#                             Item.WPFobject_("ListBoxEditItem", '', Contain).Click()
#                     elif Contain == '':
#                             Item.WPFobject_("ListBoxEditItem", Contain,1).Click()
#                     else:
#                             if SubItem.Exists:
#                                     SubItem.Click()
#                             else:
#                                     Item.WPFobject_("ListBoxEditItem", "", 1).Click()
            
#                     ListBox.Click()
            
#             except Exception as exp:
#                     self.log_info.Info('ListBoxEditItem - type:' + str(exp))
#                     if ListBox != None and hasattr(ListBox, 'Name'):
#                             self.Testresult('ListBoxEditItem '  + ListBox.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:                        
#                             self.Testresult('ListBoxEditItem: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))                
# #--
# #...
# #-- 
#     def SelectBarItem(self, Button, Contain_0 = '', Contain_1 = None, IsRaiseException = True, Condition = True, FindPropertyItem = 'Content.OleValue'):

#             try:
    
#                     if not Condition:
#                             if IsRaiseException:
#                                     raise ProjectException.cobject_IsDisabled()
#                             else:
#                                     return
                            
#                     self.ClickButton(Button)
                    
#                     Delay(50)
    
#                     Item = object_s_ContextMenu.PopupMenuBarControl
                    
#                     self.wait_for_availability(Item, method = 'SelectBarItem->' + str(Contain_0))
            
#                     SubItem = Item.FindChildEx(FindPropertyItem,Contain_0,5)

#                     if SubItem != None:
#                             if hasattr(SubItem, 'Enabled'):
#                                     if not SubItem.Enabled:
#                                             raise ProjectException.cobject_IsDisabled()
            
#                     if isinstance(Contain_0, int):
#                             if Contain_0 == 0 :
#                                     Contain_0 = 1                
#                             Item.WPFobject_("BarItemLinkInfo", '', Contain_0).Click()
#                     elif Contain_0 == '':
#                             Item.WPFobject_("BarItemLinkInfo", Contain_0,1).Click()
#                     else:
#                             if SubItem.Exists:
#                                     SubItem.Click()
#                             else:
#                                     Item.WPFobject_("BarItemLinkInfo", "",1).Click()
                            
#                     Delay(1000)
                    
#                     if Contain_1 != None:
# #                                Contain_1 = object_s_ContextMenu.ColumnControl_0
            
# #                                #SubItem = Item.FindChildEx('WPFControlText',Contain_1,500)
# #                                SubItem = Item.FindChildEx('Content.OleValue',Contain_1,500)
# #
# #                                if isinstance(Contain_1, int):
# #                                        if Contain_1 == 0 :
# #                                                Contain_1 = 1                
# #                                        Item.WPFobject_("BarItemLinkInfo", '', Contain_1))
# #                                elif Contain_1 == '':
# #                                        Item.WPFobject_("BarItemLinkInfo", Contain_1,1))
# #                                else:
# #                                        if SubItem.Exists:
# #                                                SubItem)
# #                                        else:
# #                                                Item.WPFobject_("BarItemLinkInfo", "",1))

# #Now I donot find a way to recognise seconde object_ instance first object_ therefor I create New object_. In Menu I find other way to solve this Problem but hire not working
# #I have use , FindPropertyItem = 'Content.OleValue' Check first what is Propertyname then send it optional


#                             self.wait_for_availability(Contain_1, counter = 3, method = 'SelectBarItem->' + str(Contain_1))
                            
#                             if hasattr(SubItem, 'Enabled'):
#                                     if not SubItem.Enabled:
#                                             raise ProjectException.cobject_IsDisabled()
                            
#                             Contain_1.Click(5,5)
                  
#                     return True       
               
#             except Exception as exp:
#                     self.log_info.Info('SelectBarItem - type:' + str(exp))
#                     if Button != None and hasattr(Button, 'Name'):
#                             self.Testresult('SelectBarItem '  + Button.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('SelectBarItem: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))  
#                     if IsRaiseException:
#                               raise ProjectException.cReturn()
#                     else:
#                             return False
# #--
# #...
# #-- 
#     def SelectContextMenueBarItem(self, Contain = '', Contain_1 = '', object_ = None, FindPropertyItem = 'Content.OleValue'):

#             try:
    
#                     Delay(50)
    
#                     if object_ != None:
#                             object_.ClickCellR()
            
#                             Delay(50)
    
#                     Item = object_s_ContextMenu.PopupMenuBarControl
                            
#                     self.wait_for_availability(Item, method = 'SelectContextMenueBarItem->' + str(Contain))
            
#                     SubItem = Item.FindChildEx(FindPropertyItem, Contain, 5)

#                     if isinstance(Contain, int):
#                             if Contain == 0 :
#                                     Contain = 1                
#                             Item.WPFobject_("BarItemLinkInfo", '', Contain).Click()
#                     elif Contain == '':
#                             Item.WPFobject_("BarItemLinkInfo", Contain,1).Click()
#                     else:
#                             if SubItem.Exists:
#                                     SubItem.Click()
#                             else:
#                                     Item.WPFobject_("BarItemLinkInfo", "",1).Click()
                                    
#                     Delay(1000)

#                     if Contain_1 != '':
#                             if isinstance(Contain_1, str):
#                                     object_s_ContextMenu.PopupMenuBarControl.RefreshMappingInfo()
#                                     Item = object_s_ContextMenu.PopupMenuBarControl
#                                     self.wait_for_availability(Item, method = 'SelectContextMenueBarItem->' + str(Contain_1))
            
#                                     Contain_1 = Contain + '|    ' + Contain_1
                            
#                                     SubItem = Item.FindChildEx(FindPropertyItem, Contain_1, 10)

#                                     if isinstance(Contain_1, int):
#                                             if Contain_1 == 0 :
#                                                     Contain_1 = 1                
#                                             Item.WPFobject_("BarItemLinkInfo", '', Contain_1).Click()
#                                             return True
                                            
#                                     elif Contain_1 == '':
#                                             Item.WPFobject_("BarItemLinkInfo", Contain_1,1).Click()
#                                             return True
#                                     else:
#                                             if SubItem.Exists:
#                                                     SubItem.Click()
#                                                     return True
#                                             else:
#                                                     Item.WPFobject_("BarItemLinkInfo", "",1).Click()
#                                                     return True
                                                    
#                                     return False
                                                    
#                             elif Contain_1 != None:
#                                     if Contain_1.Exists:
#                                             self.wait_for_availability(Contain_1, counter = 3, method = 'SelectContextMenueBarItem->' + str(Contain_1))
#                                     Contain_1.Click()
                  
#                                     return True
#                             return False
                            
                            
                            
#             except Exception as exp:
#                     self.log_info.Info('SelectContextMenueBarItem - type:' + str(exp))
#                     self.Testresult('SelectContextMenueBarItem: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
# #--
# #...
# #-- 
#     def SelectContextMenueStrip(self, Contain_0 = '', Contain_1 = '', Contain_2 = '', ContextMenu_0 = None, ContextMenu_1 = None, ContextMenu_2 = None, Counter = 1000, IsRaiseException = True):

#             try:
    
# #                        if Contain_2 != '':
# #                                raise ProjectException.cReturn() 
                    
#                     Delay(Counter)
                    
#                     Index_0 = 1
#                     Index_1 = 1
#                     Index_2 = 1
#                     Delay(50)

#                     if ContextMenu_0 == None:
#                             ContextMenuStrip_0 = object_s_ContextMenu.Generalcms_0
#                             if ContextMenuStrip_0 == None:
#                                     ContextMenuStrip_0 = object_s_ContextMenu.Generalcms_1
#                     else:
#                             ContextMenuStrip_0 = ContextMenu_0
            
#                     Delay(Counter)
                    
#                     self.wait_for_availability(ContextMenuStrip_0, method = 'SelectContextMenueStrip->' + str(Contain_0))
                    
#                     Height = ContextMenuStrip_0.Height
#                     Width = ContextMenuStrip_0.Width
#                     Count = ContextMenuStrip_0.get_Items().Count
#                     IndividualHeight_a = Height / Count / 2
#                     IndividualHeight_a = math.floor(IndividualHeight_a)

#                     for Index_0 in range(1,Count + 1,1):
#                             if Index_0 < 2:
#                                     IndividualHeight = IndividualHeight_a 
#                             else:
#                                     IndividualHeight = IndividualHeight_a * 2
                    
#                             Item = ContextMenuStrip_0.GetItemAt(Width/2, IndividualHeight * Index_0 - 4)
#                             if Item != None:
#                                     if ContextMenuStrip_0.GetItemAt(Width/2, IndividualHeight * Index_0 - 4).Text.OleValue == Contain_0:
#                                             if hasattr(Item, 'Enabled'):
#                                                     if not Item.Enabled and IsRaiseException:
#                                                             raise ProjectException.cReturn()
                                    
#                                             ContextMenuStrip_0.Click(Width/2, IndividualHeight * Index_0 - 4)
                                            
#                                             if Contain_1 != '':
#                                                     Delay(Counter)
#                                                     if ContextMenu_1 == None:
#                                                             ContextMenuStrip_1 = object_s_ContextMenu.Generalcms_0.activeDropDowns_2.Item[0]
#                                                     else:
#                                                             ContextMenuStrip_1 = ContextMenu_1
                                                            
#                                                     Delay(Counter)
                                                            
#                                                     self.wait_for_availability(ContextMenuStrip_1, method = 'SelectContextMenueStrip->' + str(Contain_1))
                                                    
#                                                     Height_1 = ContextMenuStrip_1.Height
#                                                     Width_1 = ContextMenuStrip_1.Width
#                                                     Count_1 = ContextMenuStrip_1.get_Items().Count
#                                                     IndividualHeight_1a = Height_1 / Count_1 / 2
#                                                     IndividualHeight_1a = math.floor(IndividualHeight_1a)
                                                    
#                                                     for Index_1 in range(1,Count_1 + 1,1):
#                                                             if Index_1 == 1:
#                                                                     IndividualHeight_1 = IndividualHeight_1a 
#                                                             else:
#                                                                     IndividualHeight_1 = IndividualHeight_1a * 2
                                                                    
#                                                             Item_1 = ContextMenuStrip_1.GetItemAt(Width_1/2, IndividualHeight_1 * Index_1 - 4)
                                                            
#                                                             if Item_1 != None:
                                                            
#                                                                     if ContextMenuStrip_1.GetItemAt(Width_1/2, IndividualHeight_1 * Index_1 - 4).Text.OleValue == Contain_1:
#                                                                             if hasattr(Item_1, 'Enabled'):
#                                                                                     if not Item_1.Enabled and IsRaiseException:
#                                                                                             raise ProjectException.cReturn()
                                                                            
#                                                                             MouseX = ContextMenuStrip_1.Left
#                                                                             MouseY = ContextMenuStrip_1.Top
#                                                                             Sys.Desktop.MouseDown(VK_LBUTTON , MouseX + Width_1/2, MouseY + IndividualHeight_1 * Index_1 - 4)
#                                                                             Sys.Desktop.MouseUp(VK_LBUTTON , MouseX + Width_1/2, MouseY + IndividualHeight_1 * Index_1 - 4)
                                                                            
                                                                            
#                                                                             Delay(1000)
                                                                            
#                                                                             if Contain_2 != '':
#                                                                                     Delay(Counter)
#                                                                                     if ContextMenu_2 == None:
#                                                                                             ContextMenuStrip_2 = Aliases.JTL_WAWi.cms_Drop
#                                                                                     else:
#                                                                                             ContextMenuStrip_2 = ContextMenu_2
                                                            
#                                                                                     ContextMenuStrip_2.RefreshMappingInfo()
#                                                                                     ContextMenuStrip_2.Refresh()
                                                                                    
#                                                                                     Delay(Counter)
                                                    
#                                                                                     self.wait_for_availability(ContextMenuStrip_2, method = 'SelectContextMenueStrip->' + str(Contain_2))
                                                                                    
#                                                                                     Height_2 = ContextMenuStrip_2.Height
#                                                                                     Width_2 = ContextMenuStrip_2.Width
#                                                                                     Count_2 = ContextMenuStrip_2.Items.Count
#                                                                                     IndividualHeight2_a = Height_2 / Count_2 / 2
#                                                                                     IndividualHeight2_a = math.floor(IndividualHeight2_a)
                                                    
#                                                                                     for Index_2 in range(1,Count_2 + 1,1):
#                                                                                             if Index_2 == 1:
#                                                                                                     IndividualHeight_2 = IndividualHeight2_a
#                                                                                             else:
#                                                                                                     IndividualHeight_2 = IndividualHeight2_a * 2 
                                                                                                    
#                                                                                             Item_2 = ContextMenuStrip_2.GetItemAt(Width_2/2, IndividualHeight_2 * Index_2 - 1)
                                                            
#                                                                                             if Item_2 != None:
#                                                                                                     if ContextMenuStrip_2.GetItemAt(Width_2/2, IndividualHeight_2 * Index_2 - 1).Text.OleValue == Contain_2:
#                                                                                                             if hasattr(Item, 'Enabled'):
#                                                                                                                     if not Item.Enabled and IsRaiseException:
#                                                                                                                             raise ProjectException.cReturn()
                                                                                                                                           
                                                                                                                                
#                                                                                                             MouseX = ContextMenuStrip_2.Left
#                                                                                                             MouseY = ContextMenuStrip_2.Top
#                                                                                                             Sys.Desktop.MouseDown(VK_LBUTTON , MouseX + Width_2/2, MouseY + IndividualHeight_2 * Index_2 - 1)
#                                                                                                             Sys.Desktop.MouseUp(VK_LBUTTON , MouseX + Width_2/2, MouseY + IndividualHeight_2 * Index_2 - 1)
#                                                                                                             return
                                                                                    
#                                                                                             Index_2 +=1
                                                                                            
#                                                                             else:
#                                                                                     return
                                                                                                    
#                                                     Index_1 += 1
                                                    
#                                             else:
#                                                     return

#                             Index_0 += 1

#             except Exception as exp:
#                     self.log_info.Info('SelectContextMenueStrip - type:' + str(exp))
#                     self.Testresult('SelectContextMenueStrip: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     if IsRaiseException:
#                               raise ProjectException.cReturn()
#                     else:
#                             return False
                            
# #--
# #...
# #-- 
#     def StateCheckBoxInTreeView(self, TreeView, Contain = True, ContainX = 1, ContainY = 1, WPFLevel = 1):

#             try:
    
#                     if not self.wait_for_availability(TreeView, counter = 3, method = 'StateCheckBoxInTreeView->' + str(Contain)):
#                             raise ProjectException.cobject_IsNotExist()  
                                    
#                     if isinstance(Containx, int) and isinstance(ContainY, int):
#                             CheckState = TreeView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", '', ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("LayoutGroup", "", 1).WPFobject_("CheckEdit", "", 1).get_IsChecked()

#                             if Contain == CheckState:
#                                     return
#                             else:
#                                     TreeView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", '', ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("LayoutGroup", "", 1).WPFobject_("CheckEdit", "", 1).Click()
                                    

#             except Exception as exp:
#                     self.log_info.Info('SelectCheckBoxInTreeView - type:' + str(exp))
#                     if TreeView != None and hasattr(TreeView, 'Name'):
#                             self.Testresult('SelectCheckBoxInTreeView '  + TreeView.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:                        
#                             self.Testresult('SelectCheckBoxInTreeView: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
# #--
# #...
# #-- 
#     def SelectCheckBoxInTableView(self, TableView, ListView = None, Contain = True, ContainX = 1, ContainY = 1, WPFLevel = 1, IsHasHierarchy = True):

#             try:
    
#                     if not Contain:
#                             return
                            
#                     if not self.wait_for_availability(TableView, counter = 3, method = 'SelectCheckBoxInTableView->' + str(Contain)):
#                             raise ProjectException.cobject_IsNotExist() 
                    
#                     if not IsHasHierarchy:
#                             TableView.ClickCell(Containx, ContainY)
#                             return
                            
#                     if ListView == None:
#                             ListView = TableView
                    
#                     if isinstance(Containx, int) and isinstance(ContainY, int):
                                    
#                             if ListView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", '', ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("Grid", "", 1).WPFobject_("CheckEdit", "", 1).Exists:
                            
#                                     Checkobject_ = ListView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", '', ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("Grid", "", 1).WPFobject_("CheckEdit", "", 1)
                            
#                                     CheckState = Checkobject_.get_IsChecked()                                
                            
#                                     if Contain == CheckState:
#                                             return
#                                     else:
#                                             Checkobject_.Click()
                                    

#                             elif ListView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("InplaceBaseEdit", "", 1).Exists:
                                    
#                                     Checkobject_ = ListView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("InplaceBaseEdit", "", 1)
                                    
#                                     CheckState = Checkobject_.CalcIsChecked()
                                    
#                                     if CheckState != None:
#                                             CheckState = Checkobject_.CalcIsChecked().OleValue
#                                     else:
#                                             return
                                            
#                                     if Contain == CheckState:
#                                             return
#                                     else:
#                                             Checkobject_.Click()
#                                             Delay(25)
#                                             Checkobject_.Click()
                                            
#                             else:
#                                     ListView.ClickItem(Containx, ContainY)

#             except Exception as exp:
#                     self.log_info.Info('SelectCheckBoxInTableView - type:' + str(exp))
#                     if TableView != None and hasattr(TableView, 'Name'):
#                             self.Testresult('SelectCheckBoxInTableView '  + TableView.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:                        
#                             self.Testresult('SelectCheckBoxInTableView: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
# #--
# #...
# #-- 
#     def SelectComboboxItemInTableView(self, TableView, ListView = None, Contain = 1, ContainX = 1, ContainY = 1, WPFLevel = 1, WaitDelay = 50):

#             try:
    
#                     Combobox = None
                    
#                     if not self.wait_for_availability(TableView, counter = 3, method = 'SelectComboboxItemInTableView->' + str(Contain)):
#                             raise ProjectException.cobject_IsNotExist() 
                            
#                     TableView.Click()
                    
#                     if ListView == None:
#                             ListView = TableView

                                                    
#                     if isinstance(Containx, int) and isinstance(ContainY, int):
#                             if ListView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("Grid", "", 1).Exists:
#                                     Combobox = ListView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("Grid", "", 1).WPFobject_("ComboBoxEdit", "", 1)

#                                     ToggleStateButton = Combobox.FindChildEx('WPFControlName', 'ButtonContainer',10)
                                    
                                    

#                             elif ListView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("PART_Editor").Exists:
#                                     Combobox = ListView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("PART_Editor")
                                            
#                                     Combobox.Click()
#                                     Delay(WaitDelay)
#                                     Combobox.Click()
#                                     Delay(WaitDelay)                                        
                                            
#                                     ToggleStateButton = Combobox.WPFobject_("ButtonsControl", "", 2).WPFobject_("ButtonContainer", "", 1).WPFobject_("DXBorder", "", 1).WPFobject_("PART_Item")
                                          
                                      
#                             elif ListView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("ComboBoxEdit", "", 1).Exists:
#                                     Combobox = ListView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("ComboBoxEdit", "", 1)

#                                     Combobox.Click()
#                                     Delay(WaitDelay)
#                                     Combobox.Click()
#                                     Delay(WaitDelay)
                                                                            
#                                     ToggleStateButton = Combobox.WPFobject_("ButtonsControl", "", 2).WPFobject_("ButtonContainer", "", 1).WPFobject_("DXBorder", "", 1).WPFobject_("PART_Item")                                

#                     if Combobox == None:
#                             raise ProjectException.cobject_IsNotExist() 
                                                                                    
#                     if hasattr(Combobox, 'DropDown'):
#                             Combobox.DropDown()
                                    
#                     elif ToggleStateButton.Exists:
#                             ToggleStateButton.Click()
                                    
#                     else:
#                             Combobox.Click()
                                    
#                     Delay(WaitDelay)
                           
#                     Item = Aliases.JTL_WAWi.Popup.Root.PopupContentControl
                    
#                     if not Item.Exists or Item == None :
#                             Item = Combobox.PopupElement
#                             Delay(WaitDelay)

#                     if Contain == 0 :
#                             Contain = 1
                                            
#                     if Item.WPFobject_("ComboBoxEditItem", '', Contain).Exists:
#                             if isinstance(Contain, int):                                
#                                     Item.WPFobject_("ComboBoxEditItem", '', Contain).Click()
#                             elif Contain == '':
#                                     Item.WPFobject_("ComboBoxEditItem", Contain,1).Click()
#                             else:
#                                     if Item.WPFobject_("ComboBoxEditItem", Contain).Exists:
#                                             Item.WPFobject_("ComboBoxEditItem", Contain).Click()
#                                     else:
#                                             Item.WPFobject_("ComboBoxEditItem", '', 1).Click()
                                            
                                            
#                     if isinstance(Contain, int): 
#                             if Item.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", Contain).WPFobject_("CellsControl", "", 1).WPFobject_("LightweightCellEditor", "", 1).WPFobject_("InplaceBaseEdit", "", 1).Exists:
#                                     Item.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", Contain).WPFobject_("CellsControl", "", 1).WPFobject_("LightweightCellEditor", "", 1).WPFobject_("InplaceBaseEdit", "", 1).Click()

#                     if hasattr(Combobox, 'CloseUp'): 
#                             Combobox.CloseUp()
            
#             except Exception as exp:
#                     self.log_info.Info('SelectComboboxItemInTableView - type:' + str(exp))
#                     if TableView != None and hasattr(TableView, 'Name'):
#                             self.Testresult('SelectComboboxItemInTableView '  + TableView.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:                        
#                             self.Testresult('SelectComboboxItemInTableView: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
# #--
# #...
# #-- 
#     def SelectDateTimeInTableView(self, TableView, ListView = None, Contain = 1, ContainX = 1, ContainY = 1, WPFLevel = 1):

#             try:
    
#                     if not self.wait_for_availability(TableView, counter = 3, method = 'SelectDateTimeInTableView->' + str(Contain)):
#                             raise ProjectException.cobject_IsNotExist() 
                            
#                     TableView.Click()
                    
#                     if ListView == None:
#                             ListView = TableView
                    
#                     if isinstance(Containx, int) and isinstance(ContainY, int):
#                             DateTime = ListView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("DateEdit", "", 1)
            
#                     Delay(50)
#                     DateTime.Refresh()
#                     DateTime.set_DateTime(Contain)
                                    
#             except Exception as exp:
#                     self.log_info.Info('SelectDateTimeInTableView - type:' + str(exp))
#                     if TableView != None and hasattr(TableView, 'Name'):
#                             self.Testresult('SelectDateTimeInTableView '  + TableView.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:                        
#                             self.Testresult('SelectDateTimeInTableView: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
# #--
# #...
# #-- 
#     def SetTextInTableView(self, TableView, ListView = None, Contain = 1, ContainX = 1, ContainY = 1, WPFLevel = 1, ClickX = '', ClickY = ''):

#             try:
    
#                     if not self.wait_for_availability(TableView, counter = 3, method = 'SetTextInTableView->' + str(Contain)):
#                             raise ProjectException.cobject_IsNotExist()
                            
#                     if ClickX == '':
#                             ClickX = ContainX
                            
#                     if ClickY == '':
#                             ClickY = ContainY                                
                             
#                     TableView.Click()
                    
#                     if ListView == None:
#                             ListView = TableView
#                             ListView.DblClickItem(Clickx, ClickY)
#                     else:
#                             if hasattr(TableView, 'DblClickCell'):
#                                     TableView.DblClickCell(Clickx, ClickY)
#                             else:
#                                     TableView.ClickCell(Clickx, ClickY)
#                                     Delay(25)
#                                     TableView.ClickCell(Clickx, ClickY)
                    
                    
#                     if isinstance(Containx, int) and isinstance(ContainY, int):
#                             if ListView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("InplaceBaseEdit", "", 1).Exists:
#                                     TextBox = ListView.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", ContainX).WPFobject_("CellsControl", "", ContainY).WPFobject_("LightweightCellEditor", "", WPFLevel).WPFobject_("InplaceBaseEdit", "", 1)
#                                     Delay(50)
                    
#                                     TextBox.WPFobject_("TextEdit", "", 1).Keys(Contain)
                            
#                             elif ListView.WinFormsobject_("FloatCellEditor", "").WinFormsobject_("UpDownEdit", "").Exists:
#                                     TextBox = ListView.WinFormsobject_("FloatCellEditor", "").WinFormsobject_("UpDownEdit", "")
#                                     Delay(50)
                                    
#                                     TextBox.Keys(Contain)

#             except Exception as exp:
#                     self.log_info.Info('SetTextInTableView - type:' + str(exp))
#                     if TableView != None and hasattr(TableView, 'Name'):
#                             self.Testresult('SetTextInTableView '  + TableView.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('SetTextInTableView: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
# #--
# #...
# #-- 
#     def SetTextInListView(self, ListView, Contain = '', X = 0, Y = 0, IsClear = False):

#             try:
                    
#                     if not self.wait_for_availability(ListView, counter = 3, method = 'SetTextInListView->' + str(Contain)):
#                             raise ProjectException.cobject_IsNotExist() 
                    
#                     ListView.DblClickItem(X, Y)
                    
#                     Delay(50)
                    
#                     if ListView.WinFormsobject_("TextBox", "").Exists:
#                             TextBox = ListView.WinFormsobject_("TextBox", "")
#                             TextBox.Click()
#                             Delay(50)
    
#                             if IsClear:
#                                     TextBox.SetText('')
                            
#                             TextBox.Keys(Contain)
            
#             except Exception as exp:
#                     if ListView != None and hasattr(ListView, 'Name'):
#                             self.Testresult('SetTextInListView '  + ListView.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:                
#                             self.Testresult('SetTextInListView: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
# #--
# #...
# #-- 
#     def ClickItemComboboxInListView(self, ListView, Contain = '', X = 0, Y = 0):

#             try:
                    
#                     if not self.wait_for_availability(ListView, counter = 3, method = 'ClickItemComboboxInListView->' + str(Contain)):
#                             raise ProjectException.cobject_IsNotExist() 
                    
#                     ListView.DblClickItem(X, Y)
                    
#                     Delay(50)
                    
#                     if ListView.WinFormsobject_("jtlListViewExFilterComboBox", "").Exists:
#                             ComboBox = ListView.WinFormsobject_("jtlListViewExFilterComboBox", "")
#                             ComboBox.ClickItem(Contain)
#                             Delay(50)
#                     elif Aliases.JTL_WAWi.ComboLBox.Exists:
#                             ComboBox = Aliases.JTL_WAWi.ComboLBox
#                             ListView.ClickItem(X, Y)
#                             ComboBox.ClickItem(Contain)
#                             Delay(50)
                            
                                            
#             except Exception as exp:
#                     if ListView != None and hasattr(ListView, 'Name'):
#                             self.Testresult('ClickItemComboboxInListView '  + ListView.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('ClickItemComboboxInListView: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
# #--
# #...
# #-- 
#     def ClickButton(self, Button, IsRaiseException = False, Condition = True, IsSetFocus = False, Delay = 5, is_report = True, counter = 3):

#             try:
    
#                     Delay(Delay)
                    
#                     if not Condition:
#                             return False
                            
#                     if not self.wait_for_availability(Button, counter = counter, is_report = is_report, method = 'ClickButton'):
#                             raise ProjectException.cobject_IsNotExist()
                    
#                     if not Button.Visible:
#                             raise ProjectException.cobject_IsNotExist()
                    
#                     if not Button.Exists:
#                             raise ProjectException.cobject_IsNotExist()
                    
#                     if not Button.Enabled:
#                             self.Testresult('Button ' + Button.Name + ' :', TypeOfresultobject_ = 'object_s') 
#                             raise ProjectException.cobject_IsDisabled()
                                                   
#                     if IsSetFocus:
#                             if hasattr(Button, 'SetFocus'):
#                                     Button.SetFocus()
#                                     Delay(50)                        
                         
#                     self.ChkPoint(Button, 'ClickButton', 'self')                                        
                                                                  
#                     if hasattr(Button, 'ClickButton'):
#                             Button.ClickButton()
#                     else:
#                             Button.Click()                                
                                 
#                     Delay(Delay)
                                          
#                     return True
                    
#             except Exception as exp:
#                     self.log_info.Info('Button:' + str(exp))
#                     if Button != None and hasattr(Button, 'Name'):
#                             self.Testresult('ClickButton '  + Button.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:                        
#                             self.Testresult('ClickButton: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
                    
#                     if IsRaiseException:
#                               raise ProjectException.cReturn()
#                     else:
#                             return False
# #--
# #...
# #-- 
#     def SelectButtonPopupItem(self, object_ = None, Contain = '', IsRaiseException = True):

#             try:
    
#                     Delay(50)
    
#                     if object_ == None:
#                             raise ProjectException.cobject_IsNotExist()
                            
#                     self.wait_for_availability(object_, counter = 3, method = 'SelectButtonPopupItem->' + str(Contain))
                    
#                     if IsRaiseException and not object_.Enabled:
#                               raise ProjectException.cobject_IsDisabled()
                    
#                     object_.ClickR()
            
#                     Delay(250)
    

#                     ContextMenuStrip = object_.StripPopupMenu
                            
#                     if hasattr(ContextMenuStrip, 'Items'):
#                             if hasattr(ContextMenuStrip.Items, 'Enabled'):
#                                     if not ContextMenuStrip.Items[Contain].Enabled:
#                                             self.Testresult('PopupItem : ', TypeOfresultobject_ = 'object_s') 
#                                             raise ProjectException.cobject_IsDisabled()
                            
#                     if Contain == '':
#                             ContextMenuStrip.Click()
#                     else:
#                             ContextMenuStrip.Click(Contain)
                            
#             except Exception as exp:
#                     self.log_info.Info('SelectButtonPopupItem - type:' + str(exp))
#                     if object_ != None and hasattr(object_, 'Name'):
#                             self.Testresult('SelectButtonPopupItem '  + object_.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('SelectButtonPopupItem: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))                          
#                     raise ProjectException.cTestAgin()     
# #--
# #...
# #-- 
#     def StateCheckBox(self, CheckBox, State = True):

#             try:
    
#                     if not self.wait_for_availability(CheckBox, counter = 3, method = 'StateCheckBox->' + str(State)):
#                             raise ProjectException.cobject_IsNotExist() 
                    
#                     if not CheckBox.Exists:
#                             raise ProjectException.cobject_IsNotExist()
                    
#                     if not CheckBox.Enabled:
#                             self.Testresult('Button ' + CheckBox.Name + ' :', TypeOfresultobject_ = 'object_s') 
#                             raise ProjectException.cobject_IsDisabled()
                    
#                     Delay(50)
                            
#                     if hasattr(CheckBox, 'wState'):
#                             if State:
#                                     CheckBox.wState = cbChecked 
#                             else:
#                                     CheckBox.wState = cbUnchecked
                                    
#                     elif hasattr(CheckBox, 'get_IsChecked'):
#                             if CheckBox.get_IsChecked().OleValue:
#                                     if State:
#                                             return True
#                                     else:
#                                             CheckBox.Click()
#                                             return True
#                             else:
#                                     if State:
#                                             CheckBox.Click()
#                                             return True
#                                     else:
#                                             return True
#                     else:
#                             CheckBox.Click()
                            
#                     self.ChkPoint(CheckBox, 'StateCheckBox', 'self') 
                                                   
#                     return True
                    
#             except Exception as exp:
#                     self.log_info.Info('StateCheckBox: ' + str(exp))
#                     if CheckBox != None and hasattr(CheckBox, 'Name'):
#                             self.Testresult('StateCheckBox '  + CheckBox.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))                  
#                     else:
#                             self.Testresult('StateCheckBox: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))                  
#                     return False
# #--
# #...
# #-- 
#     def ClickItem(self, object_, X = 0, Y = '', IsSetFocus = False, FindPropertyItem = 'Content.OleValue'):

#             try:
    
#                     if not self.wait_for_availability(object_, counter = 3, method = 'ClickItem->' + str(X)):
#                             raise ProjectException.cobject_IsNotExist() 
                    
#                     if not object_.Exists:
#                             raise ProjectException.cobject_IsNotExist()
                    
#                     if not object_.Enabled:
#                             self.Testresult('Button ' + object_.Name + ' :', TypeOfresultobject_ = 'object_s') 
#                             raise ProjectException.cobject_IsDisabled()
                    
#                     if IsSetFocus:
#                             object_.SetFocus()
                    
#                     if hasattr(object_, 'ClickItem'):
                    
#                             #ListView
#                             if hasattr(object_, 'wRowCount'):
#                                     if isinstance(X, int):
#                                             if object_.wRowCount != None:
#                                                     if object_.wRowCount < X or object_.wRowCount == 0:
#                                                             raise ProjectException.cEingabeIstFalsch()
#                                     else:
#                                             if hasattr(object_, 'FindItemWithText'):
#                                                     if object_.FindItemWithText(X) == None:
#                                                             raise ProjectException.cEingabeIstFalsch()                                                                                                                                
                                            
#                                     if Y == '':
#                                             object_.ClickItem(X)
#                                     else:
#                                             object_.ClickItem(X, Y)        
                                    
#                             #Combo        
#                             if hasattr(object_, 'wItemCount'):
#                                     if isinstance(X, int):
#                                             if object_.wItemCount != None:
#                                                     if object_.wItemCount < X or object_.wItemCount == 0:
#                                                             raise ProjectException.cEingabeIstFalsch()
#                                     else:
#                                             if hasattr(object_, 'FindItemWithText'):
#                                                     if object_.FindItemWithText(X) == None:
#                                                             raise ProjectException.cEingabeIstFalsch()                                                                
                                                            
#                                     if Y == '':
#                                             object_.ClickItem(X)
#                                     else:
#                                             object_.ClickItem(X, Y)   

#                     #TableView
#                     elif hasattr(object_, 'ClickCell'):
#                             if hasattr(object_, 'wRowCount'):
#                                     if isinstance(X, int):
#                                             if object_.wRowCount != None:
#                                                     if object_.wRowCount < X or object_.wRowCount == 0:
#                                                             raise ProjectException.cEingabeIstFalsch()
#                                     else:
#                                             if hasattr(object_, 'FindItemWithText'):
#                                                     if object_.FindItemWithText(X) == None:
#                                                             raise ProjectException.cEingabeIstFalsch()                                                                
                                            
#                                     if Y == '':
#                                             #GridControl
#                                             if hasattr(object_, 'ClickRowIndicator'):
#                                                     if isinstance(X, int):
#                                                             object_.ClickRowIndicator(X)
#                                                     else:
#                                                             try:
#                                                                     object_.ClickCell(X, 0)
#                                                             except Exception as exp:
#                                                                     object_.Click(30, 30)
#                                     else:
#                                             try: 
#                                                     object_.ClickCell(X, Y)
#                                             except Exception as exp:
#                                                     object_.Click(30, 30)
                                            
#                     #KundenTableView
#                     elif hasattr(object_, 'Click'):
#                             object_.Click()
                            
#                             Delay(500)
                            
#                             if X == '':
#                                     object_.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", 1).WPFobject_("RowIndicator", "", 1).Click()

#                             #TableView
#                             elif hasattr(object_, 'HierarchyPanel'):
#                                     object_.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", X).WPFobject_("RowIndicator", "", 1).Click()
                                    
#                             #Combobox
#                             elif Aliases.JTL_WAWi.Popup.Root.PopupContentControl.Exists:
#                                     Item = Aliases.JTL_WAWi.Popup.Root.PopupContentControl
                                    
#                                     if X == '':
#                                             Item.WPFobject_("ComboBoxEditItem", "", 1).Click()
                                    
#                                     else:
#                                             if hasattr(Item, 'FindItemWithText'):
#                                                     if object_.FindItemWithText(X) != None:
#                                                             Item.FindItemWithText(X).Click()
#                                                     else:
#                                                             raise ProjectException.cEingabeIstFalsch()
                                                            
#                                             elif hasattr(Item, 'FindChildEx'):
#                                                     if Item.FindChild(FindPropertyItem, X, 3) != None:
#                                                             SubItem = Item.FindChild(FindPropertyItem, X, 3)
#                                                     Delay(250)
#                                                     SubItem.Click()
                                            
#                             else:
#                                     object_.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", X).WPFobject_("RowIndicator", "", 1).Click()

                                            
#                     self.ChkPoint(object_, 'ClickItem', 'self')
                    
#                     return True
                    
#             except Exception as exp:
#                     self.log_info.Info('ClickItem: ' + str(exp))
#                     if object_ != None and hasattr(object_, 'Name'):
#                             self.Testresult('ClickItem '  + object_.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:                                
#                             self.Testresult('ClickItem: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))                  
#                     return False
# #--
# #...
# #-- 
#     def DblClickItem(self, object_, X = 0, Y = '', IsSetFocus = False):

#             try:
    
#                     if not self.wait_for_availability(object_, counter = 3, method = 'DblClickItem->' + str(X)):
#                             raise ProjectException.cobject_IsNotExist() 
                    
#                     if not object_.Exists:
#                             raise ProjectException.cobject_IsNotExist()
                    
#                     if not object_.Enabled:
#                             self.Testresult('Button ' + object_.Name + ' :', TypeOfresultobject_ = 'object_s') 
#                             raise ProjectException.cobject_IsDisabled()
                    
#                     if IsSetFocus:
#                             object_.SetFocus()
                    
#                     if hasattr(object_, 'DblClickItem'):
#                             #ListView
#                             if hasattr(object_, 'wRowCount'):
#                                     if isinstance(X, int):
#                                             if object_.wRowCount != None:
#                                                     if object_.wRowCount < X or object_.wRowCount == 0:
#                                                             raise ProjectException.cEingabeIstFalsch()
#                                     else:
#                                             if hasattr(object_, 'FindItemWithText'):
#                                                     if object_.FindItemWithText(X) == None:
#                                                             raise ProjectException.cEingabeIstFalsch()                                                                                                                                
                                            
#                                     if Y == '':
#                                             object_.DblClickItem(X)
#                                     else:
#                                             object_.DblClickItem(X, Y)        
                                    
#                             #Combo        
#                             if hasattr(object_, 'wItemCount'):
#                                     if isinstance(X, int):
#                                             if object_.wItemCount != None:
#                                                     if object_.wItemCount < X or object_.wItemCount == 0:
#                                                             raise ProjectException.cEingabeIstFalsch()
#                                     else:
#                                             if hasattr(object_, 'FindItemWithText'):
#                                                     if object_.FindItemWithText(X) == None:
#                                                             raise ProjectException.cEingabeIstFalsch()                                                                
                                                            
#                                     if Y == '':
#                                             object_.DblClickItem(X)
#                                     else:
#                                             object_.DblClickItem(X, Y)   

#                     #TableView
#                     elif hasattr(object_, 'DblClickCell'):
#                             if hasattr(object_, 'wRowCount'):
#                                     if isinstance(X, int):
#                                             if object_.wRowCount != None:
#                                                     if object_.wRowCount < X or object_.wRowCount == 0:
#                                                             raise ProjectException.cEingabeIstFalsch()
#                                     else:
#                                             if hasattr(object_, 'FindItemWithText'):
#                                                     if object_.FindItemWithText(X) == None:
#                                                             raise ProjectException.cEingabeIstFalsch()
                                            
#                                     if Y == '':
#                                             #GridControl
#                                             if hasattr(object_, 'ClickRowIndicator'):
#                                                     if isinstance(X, int):
#                                                             object_.ClickRowIndicator(X)
#                                                     else:
#                                                             object_.DblClickCell(X)
#                                     else:
#                                             object_.DblClickCell(X, Y)
                                            
#                     #KundenTableView
#                     elif hasattr(object_, 'DblClick'):
#                             if X == '':
#                                     object_.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", 1).WPFobject_("RowIndicator", "", 1).Click()
#                             else:
#                                     object_.WPFobject_("HierarchyPanel", "", 1).WPFobject_("RowControl", "", X).WPFobject_("RowIndicator", "", 1).Click()
                                            
#                     self.ChkPoint(object_, 'DblClickItem', 'self')
                    
#                     return True
                    
#             except Exception as exp:
#                     self.log_info.Info('DblClickItem: ' + str(exp))
#                     if object_ != None and hasattr(object_, 'Name'):
#                             self.Testresult('DblClickItem: '  + object_.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:                                
#                             self.Testresult('DblClickItem: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))                  
#                     return False   
# #--
# #...
# #-- 
#     def CheckItem(self, object_, X = 0, Y = '', Contain = True):

#             try:
    
#                     if not self.wait_for_availability(object_, counter = 3, method = 'CheckItem->' + str(X)):
#                             raise ProjectException.cobject_IsNotExist() 
                    
#                     if not object_.Exists:
#                             raise ProjectException.cobject_IsNotExist()
                    
#                     if not object_.Enabled:
#                             self.Testresult('Button ' + object_.Name + ' :', TypeOfresultobject_ = 'object_s') 
#                             raise ProjectException.cobject_IsDisabled()
                    
#                     if object_ == None:
#                             raise ProjectException.cobject_IsNotExist()        
                            
#                     object_.SetFocus()
                    
#                     if hasattr(object_, 'CheckItem'):
#                             #ListView
#                             if hasattr(object_, 'wRowCount'):
#                                     if object_.wRowCount != None:
#                                             if isinstance(X, int):
#                                                     if object_.wRowCount < X or object_.wRowCount == 0:
#                                                             raise ProjectException.cEingabeIstFalsch()
#                                             else:
#                                                     if hasattr(object_, 'FindItemWithText'):
#                                                             if object_.FindItemWithText(X) == None:
#                                                                     raise ProjectException.cEingabeIstFalsch()                                                                
                                                            
                                            
#                                     if Y == '':
#                                             object_.CheckItem(X, Contain)
#                                     else:
#                                             object_.CheckItem(X, Y, Contain)
                                            
#                             elif hasattr(object_, 'wItemCount'):   
#                                     if object_.wItemCount != None:
#                                             if isinstance(X, int):
#                                                     if object_.wItemCount < X or object_.wItemCount == 0:
#                                                             raise ProjectException.cEingabeIstFalsch()
#                                             else:
#                                                     if hasattr(object_, 'FindItemWithText'):
#                                                             if object_.FindItemWithText(X) == None:
#                                                                     raise ProjectException.cEingabeIstFalsch()
                                            
#                                     if Y == '':
#                                             object_.CheckItem(X, Contain)
#                                     else:
#                                             object_.CheckItem(X, Y, Contain)                                                                      
                                    
                                            
#                     self.ChkPoint(object_, 'CheckItem', 'self')
                    
#                     return True
                    
#             except Exception as exp:
#                     self.log_info.Info('CheckItem: ' + str(exp)) 
#                     if object_ != None and hasattr(object_, 'Name'):
#                             self.Testresult('CheckItem '  + object_.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('CheckItem: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     return False                                             
# #--
# #...
# #-- 
#     def SetText(self, TextBox, Contain = '', IsClear = True, IsEnter = False, IsUseKey = False, counter = 3, IsAbsturz = True, Delay = 50):

#             try:
            
#                     if not self.wait_for_availability(TextBox, counter = counter, method = 'SetText->' + str(Contain[:35])):
#                             raise ProjectException.cobject_IsNotExist() 
                   
#                     if not TextBox.Enabled:
#                             raise ProjectException.cobject_IsDisabled()
                                                    
#                     if hasattr(TextBox, 'Clear') and IsClear:
#                             TextBox.Clear()
                            
#                     if IsClear:
#                             TextBox.SetText('')
#                             Delay(Delay)
                                                   
#                     TextBox.Click()
#                     Delay(Delay)
                    
#                     if IsAbsturz:
#                             TextBox.Key('[Enter]')
#                             Delay(Delay)
    
#                     try:
                    
#                             _ = Contain.index('[')
#                             TextBox.Keys(Contain)
                            
#                     except Exception as exp:
                    
#                             if IsUseKey:
#                                     TextBox.DblClick()
#                                     TextBox.Keys(Contain)
#                             else:
#                                     TextBox.SetText(Contain)
                                    
#                     finally:
#                             pass
    
#                     if IsEnter:
#                             TextBox.Keys('[Enter]')
    
#                     self.ChkPoint(TextBox, 'SetText', 'self')
                    
#                     return True
            
#             except Exception as exp:
#                     if TextBox != None and hasattr(TextBox, 'Name'):
#                             self.Testresult('SetText '  + TextBox.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('SetText: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
                            
#                     return False
# #--
# #...
# #-- 
#     def SetDate(self, object_, Contain = ''):

#             try:
    
#                     if not self.wait_for_availability(object_, counter = 3, method = 'SetDate->' + str(Contain)):
#                             raise ProjectException.cobject_IsNotExist() 
                                            
#                     if Contain == '':
#                             raise ProjectException.cEingabeIstFalsch()
                                            
#                     Delay(50)
                    
#                     object_.Click()
                    
#                     if hasattr(object_, 'set_DateTime'):
#                             object_.set_DateTime(Contain)

#                     elif hasattr(object_, 'wDate'):
#                             object_.wDate = Contain
                    
#                     elif hasattr(object_, 'mDate'):
#                             object_.mDate = Contain                                
                         
#                     self.ChkPoint(object_, 'SetDate', 'self')
                    
#             except Exception as exp:
#                     if object_ != None and hasattr(object_, 'Name'):
#                             self.Testresult('SetDate '  + object_.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('SetDate: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))  
# #--
# #...
# #-- 
#     def ClickTab(self, object_, Contain = '', Delay = 500):

#             try:
    
#                     if not self.wait_for_availability(object_, counter = 3, method = 'ClickTab->' + str(Contain)):
#                             raise ProjectException.cobject_IsNotExist() 
                                            
#                     if Contain == '':
#                             raise ProjectException.cEingabeIstFalsch()
                             
#                     if hasattr(object_, 'ClickTab'):
#                             object_.ClickTab(Contain)
                            
#                     Delay(Delay)
                            
#                     self.ChkPoint(object_, 'TabName', 'self')
                    
#             except Exception as exp:
#                     if object_ != None and hasattr(object_, 'Name'):
#                             self.Testresult('ClickTab '  + object_.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('ClickTab: ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))     
# #--
# #...
# #-- 
#     def Click(self, object_, X = 5, Y = 5, IsXY = True, IsWaitFor = True, Delay = 50):

#             try:
    
#                     if IsWaitFor:
#                             if not self.wait_for_availability(object_, counter = 3, method = 'Click'):
#                                     raise ProjectException.cobject_IsNotExist() 
                    
#                     self.ChkPoint(object_, 'Click', 'self')
                                
#                     if hasattr(object_, 'Click'):
#                             if IsXY:
#                                     object_.Click(X, Y)
#                             else:
#                                     object_.Click()
                            
#                     Delay(Delay)
                    
#             except Exception as exp:
#                     if object_ != None and hasattr(object_, 'Name'):
#                             self.Testresult('Click '  + object_.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('Click ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
# #--
# #...
# #-- 
#     def ClickR(self, object_, Contain = '', CMS = None, IsWaitFor = True, Delay = 50, IsJustClickR = False):

#             try:
    
#                     if IsWaitFor:
#                             if not self.wait_for_availability(object_, counter = 3, method = 'Click->' + str(Contain)):
#                                     raise ProjectException.cobject_IsNotExist() 
                    
#                     self.ChkPoint(object_, 'ClickR', 'self')
                                
#                     Delay(Delay)
                    
#                     if hasattr(object_, 'ClickR'):
#                             object_.ClickR(5, 5)
                            
#                             Delay(Delay)
                            
#                             if IsJustClickR == False:
#                                     if CMS == None :
#                                             object_.StripPopupMenu.Click(Contain)
                                            
#                                     else:
#                                             object_.CMS.Click(Contain)
                            
#                     Delay(Delay)
                    
#             except Exception as exp:
#                     if object_ != None and hasattr(object_, 'Name'):
#                             self.Testresult('ClickR '  + object_.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('ClickR ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
# #--
# #...
# #-- 
#     def Close(self, object_, IsWaitFor = True, Delay = 50):

#             try:
    
#                     if IsWaitFor:
#                             if not self.wait_for_availability(object_, counter = 3, method = 'Close'):
#                                     raise ProjectException.cobject_IsNotExist() 
                    
#                     self.ChkPoint(object_, 'Close', 'self')
                                
#                     if hasattr(object_, 'Close'):
#                             object_.Close()
                            
#                     Delay(Delay)
                    
#             except Exception as exp:
#                     if object_ != None and hasattr(object_, 'Name'):
#                             self.Testresult('Close '  + object_.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('Close ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))                                
# #--
# #...
# #-- 
#     def DblClick(self, object_, X = 5, Y = 5, IsXY = True, IsWaitFor = True):

#             try:

#                     if IsWaitFor:
#                             if not self.wait_for_availability(object_, counter = 3, method = 'DblClick'):
#                                     raise ProjectException.cobject_IsNotExist() 
                    
#                     self.ChkPoint(object_, 'DblClick', 'self')
                                
#                     if hasattr(object_, 'DblClick'):
#                             if IsXY:
#                                     object_.DblClick(X, Y)
#                             else:
#                                     object_.DblClick()
                                    
#             except Exception as exp:
#                     if object_ != None and hasattr(object_, 'Name'):
#                             self.Testresult('DblClick '  + object_.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('DblClick ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
# #--
# #...
# #-- 
#     def TreeViewClick(self, object_, methode = 'wItems', ItemIndex = 0):

#             try:
    
#                     if not self.wait_for_availability(object_, counter = 3, method = 'TreeViewClick'):
#                             raise ProjectException.cobject_IsNotExist() 
                    
#                     self.ChkPoint(object_, 'TreeViewClick', 'self')
                                            
#                     if hasattr(object_, 'Click'):
#                             if methode == 'wItems':
#                                     object_.wItems.Item[ItemIndex].Click()
                            
#             except Exception as exp:
#                     if object_ != None and hasattr(object_, 'Name'):
#                             self.Testresult('TreeViewClick '  + object_.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('TreeViewClick ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))                                                                          
# #--
# #...
# #-- 
#     def ItemCount(self, object_):

#             try:
            
#                     if not self.wait_for_availability(object_, counter = 3, method = 'ItemCount'):
#                             raise ProjectException.cobject_IsNotExist()
    
#                     Count = 0
                    
#                     if hasattr(object_, 'wItemCount'):   
#                             if object_.wItemCount != None:
#                                     Count = object_.wItemCount
                                    
#                     elif hasattr(object_, 'wItems'):   
#                             if object_.wItems != None:
#                                     Count = object_.wItems.Count
                            
#                     elif hasattr(object_, 'wRowCount'):   
#                             if object_.wItems != None:
#                                     Count = object_.wRowCount

#                     return Count
                            
#             except Exception as exp:
#                     if object_ != None and hasattr(object_, 'Name'):
#                             self.Testresult('ItemCount '  + object_.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('ItemCount ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
# #--
# #...
# #--        
#     def ClickImage(self, Image, X = 5, Y = 5, Shift = 0, Area = "Sys.Desktop.ActiveWindow()", Delay = 150):
#             Options.Run.Timeout = 250
            
#             try:
            
#                     if not self.wait_for_availability(Image, counter = 1, just_exists = True):
#                             raise cException.cobject_IsNotExist()
                    
#                     Image.Click(X, Y, Shift, Area)
                    
#                     Delay(Delay)
                    
#             except Exception as exp:
#                     if object_ != None and hasattr(object_, 'Name'):
#                             self.Testresult('ClickImage '  + object_.Name + ': ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))
#                     else:
#                             self.Testresult('ClickImage ', TypeOfresultobject_ = 'object_s', MoreInfo = str(exp))