import os
from WAWi.Setting.TestApp import Config

#--
#...
#--
class cRecorder():
        def __init__(self):
                pass

                
                self.Form                                                              						        							= NameMapping.Sys.Process("ScreenRecorder").Window("ConsoleWindowClass", r"C:\OneDrive\Manager\ScreenRecorder.exe", 1)
                self.FFMPGForm                                                                                                                  = NameMapping.Sys.Process("ffmpeg").Window("ConsoleWindowClass", "C:\\Mad-Grb\\Apps\\ffmpeg-4.3-win64-static\\bin\\ffmpeg.exe")


                    
#--
#...
#--
        def StartRecord(self):  
            
                try:
                
                        self.Form.Close()
                        Delay(3000)
                        while Sys.WaitProcess('ScreenRecorder').Exists:
                                Sys.WaitProcess('ScreenRecorder').Terminate()
                                #TestedApps.ScreenRecorder.Terminate()
                                self.Form.Close()
                                Delay(3000)
            
                        files = os.listdir(Config.Recorder_Address)
                        for filename in files:
                            if filename.upper() == 'Row.avi'.upper():
                                    os.remove(Config.Recorder_Address + r'\Row.avi')
                                    
                        os.startfile(Config.ScreenRecorderBat)
                        Delay(3000)
                        self.Form.Minimize()
                        
                except Exception as exp:
                        Log.Warning("StartRecord: " + str(exp))
#--
#...
#--    
        def StopRecord(self):     
            
                try:       
                
                        self.Form.Close()
                        Delay(3000)
                        Sys.Process('ScreenRecorder').Terminate()
                        
                        Delay(6000)
                        
                        while Sys.WaitProcess('ScreenRecorder').Exists:
                                Sys.Process('ScreenRecorder').Terminate()
                                Delay(3000)
                        
                        FileName = os.listdir(Config.Recorder_Address)
                        os.rename(Config.Recorder_Address + '\\' + FileName[0], Config.Recorder_Address + r'\Row.avi')
                        
                        cmd = Config.bat
                        os.system(cmd)
                        
                        while Sys.WaitProcess('ffmpeg').Exists:
                                Delay(250)
                        
                        while self.FFMPGForm.Exists:
                                Delay(500)
                        Delay(500)
                        
                        files = os.listdir(Config.Recorder_Address)
                        for filename in files:
                            if filename.upper() == 'Row.avi'.upper():
                                    os.remove(Config.Recorder_Address +r'\Row.avi')
                                                
                except Exception as exp:
                        Log.Warning("StopRecord: " + str(exp))                
#--
#...
#--


