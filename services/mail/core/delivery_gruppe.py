#from AQC.Setting.TestApp import Config
#import mException
#
#class cDeliveryGruppe():
#        def __init__(cls, DeliveryGroupe = 'BugAlert'):
#                pass
#
#        cls.DeliveryGroupe                                                  = DeliveryGroupe
#                
#                
##--
##...
##--
#        @classmethod
#        def GetDeliveryAddress(cls):
#                
#                try:
#                        
#                        DeliveryGroupeListe = DeliveryGroupe.split(",")
#                        
#                        for Index in range(0,len(DeliveryGroupeListe), 1):
#                                DeliveryGroupe = DeliveryGroupeListe[Index]
#                        
#                                if cls.to_Adddress.find(DeliveryGroupe) == -1:
#                                        cls.to_Adddress = cls.to_Adddress + ', ' + DeliveryGroupe
#                                
#                                        if DeliveryGroupe == 'Admin':
#                                                cls.to_Address_list = Config.Default_Admin_Address + ', ' + cls.to_Address_list
#                                                cls.to_Address_list = Config.Default_Dev_Address + ', ' + cls.to_Address_list
#                                
#                                        if DeliveryGroupe == 'Dev':
#                                                cls.to_Address_list = Config.Default_Dev_Address + ', ' + cls.to_Address_list
#                                                
#                                        if DeliveryGroupe == 'BugAlert':
#                                                #cls.to_Address_list = Config.Default_Admin_Address + ', ' + cls.to_Address_list
#                                                cls.to_Address_list = Config.Default_Dev_Address + ', ' + cls.to_Address_list
#                                                cls.to_Address_list = Config.TC_BugAlert_Address + ', ' + cls.to_Address_list
#                                
#                except Exception as exp:
#                        Log.Warning("GetDeliveryAddress: " + str(exp))
