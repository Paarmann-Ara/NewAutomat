import imaplib
import imp
import os
import codecs
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import datetime
import smtplib
import shutil
import os.path
from os import path
import mDBOperation
from WAWi.Setting.TestApp import Config
from ftplib import FTP_TLS
import urllib.request as request
import mWAWiSetup
from zipfile import ZipFile
import zipfile
import socket

#--
#...
#--
class Server():
        def __init__(self):
                self.IsRun                                                                                                                      = True
                self.JObString                                                                                                                  = []
                self.Today                                                                                                                      = 'Montag'
                self.TestMeDB                                                                                                                   = True
                self.Absender                                                                                                                   = ''
                self.CommandTurn                                                                                                                = '1'
                self.IdelCounter                                                                                                                = 0
                self.ListTestMe                                                                                                                 = []
                self.IsInErstKreislaufFurTestMe                                                                                                 = True
        
                

#--
#...
#--        
        def Start(self):
    
                try:

                        LoginConf = ''
                        LoginData = None
                        TYP = ''
                        email_user = Config.TC_Address
                        email_pass = Config.TC_Password

                        self.__CheckLokalAQC()
                        
                        while True :                   

                                try:
                                
                                        self.IdelCounter += 1
                                                                              
                                        self.__ExternalLockAndCommandTurn()
                                        
                                        self.__TodysJobs()
                                        
                                        self.__SetTestPlattform()
                                        
                                        self.__ClearOneDrive()
                                        
                                        if self.IdelCounter > Config.IdelCounterToTestMe and Config.TestPlatforms == 'TC' and Config.IsTestMe:
                                                self.TestMe(Config.NumberOfTestMailToSend)
                                                self.IsInErstKreislaufFurTestMe = False
                                        
                                        if Config.IsClearBackups:
                                                self.__ClearBackups()
                                        
                                        Temp = mDBOperation.cDBOperation()
                                        WAWiVersion = Temp.DBC(SQLCommand = "USE eazybusiness;SELECT cValue FROM tOptions WHERE ckey = 'Revision'", Type = 'OnePropertyQRY') 
                                        
                                        if Config.IsUpdateToLastDevlopVersion:
                                                self.__GetAktellDevVersion(True)
                                        
                                        if WAWiVersion != Config.AktualVersion and Config.IsUpdateWAWi:
                                                self.UpdateMe()
                                                
                                        else:
                                
                                                DBmsg = Temp.DBC(Type = 'MorePropertyQRY', NumberOfFields = 2, SQLCommand = "USE AQC;SELECT TOP(1) Job_ID, JOB FROM JOBS", SQLHost = Config.AQCHost)
                        
                                                if DBmsg[0] == 'DB Fehler':
                                                        self.__CheckLokalAQC()
                                                
                                                elif DBmsg[0] != 'None' and Config.IsRunJob:
                                                        Temp.DBC(Type = 'Command', SQLCommand = "USE AQC;UPDATE JOBS SET IsStarted = 'TRUE' WHERE Job_ID = " + DBmsg[0], SQLHost = Config.AQCHost)
                                
                                                        DB_msg = DBmsg[1]
                                                        Sender = DB_msg[DB_msg.find(':') + 1 : DB_msg.find('\n')]
                                                        self.__SendConfirmationEmail(Sender)
                                                        msg = DB_msg[DB_msg.find('def'):]
                                                        aqFile.WriteToTextFile(Config.Email_Decodec_Commands_Module_Address, msg, aqFile.ctANSI, True)
                                                        
                                                        self.__RunTest()
                                                        self.IdelCounter = 0
                                                        
                                                        Delay(3300)
                                
                                                else:             
                
                                                        M = imaplib.IMAP4(Config.TC_MailServer)                
                                                        LoginConf, LoginData = M.login(email_user, email_pass)
                        
                                                        while LoginConf != 'OK':
                                                                Delay(60000)
                                                                LoginConf, LoginData = M.login(email_user, email_pass)                        
                                
                                                        TYP, MsgData = M.select('INBOX')
                        
                                                        while TYP != 'OK':
                                                                Delay(60000)
                                                                TYP, MsgData = M.select('INBOX')
                                        
                                                        CountMsg = int(MsgData[0])
                        
                                                        M.close()
                                                        M.logout()
                                                        M = None
                                
                                                        if CountMsg > 0:
                                                                self.__TurnLockOperation('Lock')
                                                                
                                                                self.__FetchCommand()
                                                                
                                                                if self.Absender != 'MAILER-DAEMON@mail.jtl-software.de':
                                                                        self.__SendConfirmationEmail(self.Absender)
                                        
                                                                        if self.IsRun:
                                                                                self.__RefreshCommand()
                                                                                
                                                                                self.__TurnLockOperation('ReleseLock')
                                                                                
                                                                                self.__ExternalLockAndCommandTurn()
                                                                                
                                                                                self.__RunTest()
                                                                                self.IdelCounter = 0
                                                                                
                                                                                Delay(3000)
                                                                
                                                                if not self.IsRun:
                                                                        self.__RefreshCommand()
                                
                                                        Delay(5000)   
                                
                                                self.IsRun = True
                        
                                        if M != None:
                                                if M.state == 'SELECTED':
                                                        M.close()
                                                if not M.sock._closed:
                                                        M.logout()
                                                M = None

                                except Exception as exp:
                                        Log.Warning("ServerStart: " + str(exp))
                                    
                                finally:
                                        pass
                                    
                except Exception as exp:
                        Log.Warning("ServerStart: " + str(exp))
#--
#...
#--      
        def TestMe(self, NumberOfTestMailToSend = -1):
    
                try:
                                
                        if NumberOfTestMailToSend == -1 or (self.IsInErstKreislaufFurTestMe and Config.IsSchicktKompleteTestfaelle):
                                self.__FillListTestMe()
                                
                                while len(self.ListTestMe) > 0:
                                        mail = self.ListTestMe.pop(0)
                                        self.__TestMe_SendMail(mail)
                                        
                        else:
                                if len(self.ListTestMe) == 0:
                                        self.__FillListTestMe()
                                        
                                while NumberOfTestMailToSend > 0:
                                        mail = self.ListTestMe.pop(0)
                                        self.__TestMe_SendMail(mail)
                                        NumberOfTestMailToSend -= 1
                                        
                except Exception as exp:
                    Log.Warning("TestMe: " + str(exp))
#--
#...
#--      
        def __FillListTestMe(self):
    
                try:

                        if len(self.ListTestMe) == 0:
                                self.RefreshMe()
                                Text = ''
                                Keeper = 0
                        
                                self.__CerateTestMeFile()
                                
                                if Config.IsUseTestToolsRepository:
                                        File = open(Config._Repository_TestToolsAddress, "r")   
                                else:
                                        File = open(Config._Repository_Address, "r")
                
                                for line in File:
                                        if line.find('$') != -1:
                                                Keeper += 1
                                                if Keeper % 2 == 0:
                                                        Text = Text + '\n#'
                                                        self.ListTestMe.append(Text)
                                                        Text = ''    
                                                        Keeper += 1                           
                                                Text = Text + '#\n' + line 
                                        if line.find('^') != -1 or line.find('~') != -1 or line.find('%') != -1:
                                                Text = Text + line 
                                File.close()
                                        
                except Exception as exp:
                    Log.Warning("__FillListTestMe: " + str(exp))
#--
#...
#--      
        def __CerateTestMeFile(self):
    
                try:
                
                        return
                
                        # Must create Textfile of Testfälle Automatcaly
                        Text = ''
                        
                        TargetList = []
                                        
                        ScriptsFile = os.listdir(Config.WAWi_AQC_Directory_Script)
                        for File in ScriptsFile:
                                TargetFile= Config.WAWi_AQC_Directory_Script + '/' + File
                                        
                                filename, file_extension = os.path.splitext(TargetFile)
                                        
                                if file_extension == '.py':
                                        TargetList.append(TargetFile)
                                                        
                        for file in TargetList:
                        
                        

                        #becuse of update in neue Version I have no time to complete it
                        
                        
                                import os, importlib, TestAllTestFalleInModule
                                try:
                
                                        Text = ''
                        
                                        ModuleList = []
                                        MethodeList = []
                                        
                                        ScriptsFile = os.listdir(Config.WAWi_AQC_Directory_Script)
                                        for File in ScriptsFile:
                                                TargetFile = Config.WAWi_AQC_Directory_Script + '/' + File
                                        
                                                filename, file_extension = os.path.splitext(TargetFile)
                                                filename = os.path.basename(filename)
                                        
                                                if file_extension == '.py'and filename.startswith("m") :
                                
                                                        ModuleList.append(filename)
                                                        
                                        for Module in ModuleList:
                        
                                                MethodeList.append([Module, TestAllTestFalleInModule.List_TestCase_In_Module(Module)])
                                                m=0
                                
                                        File = open(Config._Repository_Address, "a")
                                        
                                        File.close()
                                        
                                except Exception as exp:
                                    Log.Warning("__FillListTestMe: " + str(exp))    
    
    
    
        
                                m = os.path.basename(r'C:\OneDrive\TC\AQC\WAWi\Script\mwawi.py')
                                g=0
        
                        
                        
                        
                        
                        
                        
                
                        File = open(Config._Repository_Address, "a")
                
                        File.close()
                                        
                except Exception as exp:
                    Log.Warning("__FillListTestMe: " + str(exp))
#--
#...
#--      
        def __TestMe_SendMail(self, Body = '', To = ''):
    
                try:
    
                        Subject = 'TestTCServer'
                        Sender = Config.NoReplay_Address
                        Password = Config.NoReplay_Password
                        SmtpServer= Config.NoReply_MailServer_SMTP
                
                        To = Config.TC_Address
                
                        message = MIMEMultipart('alternative')
                        message['subject'] = Subject
                        message['From'] = Sender
                        message['To'] = To
                        
                        Body =  MIMEText(Body, 'plain')
                        
                        message.attach(Body)
                         
                        server = smtplib.SMTP(SmtpServer)
                        server.starttls()
                        server.login(Sender,Password)
                        
                        server.sendmail(Sender, To, message.as_string())
                        server.quit()
                        
                        Delay(1000)
            
                except Exception as exp:
                    Log.Warning("TestMe_SendMail: " + str(exp))
#--
#...
#--                      
        def RefreshMe(self):
    
                try:
    
                        if Config.IsRefreshMailBox:
                                email_user = Config.TC_Address
                                email_pass = Config.TC_Password
                                M = imaplib.IMAP4(Config.TC_MailServer)
                                M.login(email_user, email_pass)

                                TYP, MsgData = M.select('INBOX')
                                CountMsg = int(MsgData[0])

                                for Index in range(1, CountMsg + 1):
                                        M.store(str(Index), '+FLAGS', r'(\Deleted)')
                
                                M.expunge()
                        
                                M.close()
                                M.logout()
                                M = None
            
                        shutil.rmtree(Config.Recorder_Address)
                        os.makedirs(Config.Recorder_Address)
                        
                        self.__TestExecuteDeleteExtraFiles()
            
                except Exception as exp:
                    Log.Warning("RefreshMe: " + str(exp))
#--
#...
#--      
        def UpdateMe(self):
    
                try:
                
                        self.__TurnLockOperation('ReleseLock')
                
                        if Config.IsUpdateToLastDevlopVersion:
                                self.__GetAktellDevVersion(True)
                        
                        if Sys.WaitProcess('JTL-Wawi').Exists:
                                Sys.Process('JTL-Wawi').Terminate()
                                Delay(5000)
                        while Sys.WaitProcess('JTL-Wawi').Exists:
                                Delay(5000)
                                Sys.Process('JTL-Wawi').Terminate()
                
                        if self.TestMeDB:
                                DB_ToRestore = Config.TestMeDB
                        else:
                                DB_ToRestore = Config.DB_ToRestore
                                
                        Temp = mDBOperation.cDBOperation()
                        Temp.DBC('DB_TestMeRestore', SQLHost = Config.SQLHost)
                        
                        Delay(4800)
                        
                        while Temp.DBC('STANDARD', SQLHost = Config.SQLHost, Type = 'OnePropertyQRY') != 'ONLINE':
                                Temp.DBC('MU', SQLHost = Config.SQLHost)
                                Delay(1000)
                                Temp.DBC('DB_TestMeRestore', SQLHost = Config.SQLHost)
                                Delay(4810)
                                
                        self.__DownloadWAWiForSetup(Config.SetupVersion)
                                 
                        End = len(Config.SetupVersion) - 4                       
                        Start = Config.SetupVersion.find('1')
                        Config.SetupVersion = Config.SetupVersion[Start:End]
                        Config.TestMeVersionFolder = Config.WAWiInstallAdress + '\\' + Config.SetupVersion
                        
                        Config.TestMeVersionFolder = Config.TestMeVersionFolder.replace('\\', '/')
                        Config.WAWiInstallAdress = Config.WAWiInstallAdress.replace('\\', '/') 
                        
                        self.__SendUpdateInfo()
                        
                        Temp = mWAWiSetup.cWAWiSetup()
                        Temp.InstallWAWi()
                        
                        if os.path.exists(Config.WAWiSetup):
                                os.remove(Config.WAWiSetup)
                                
                        if os.path.exists(Config.Update_Temp_Module_Address):
                                os.remove(Config.Update_Temp_Module_Address)                                
                                
                        msg = '\ndef Start():\n' + 2*'\t' + 'Test = None\n' + 2*'\t' + 'import mWAWi' +'\n' + 2* '\t' + 'Test = mWAWi.cWAWi()\n' + 2* '\t' + 'Test.RunWAWi()\n\n'
                        with open(Config.Update_Temp_Module_Address , "a") as code:
                            code.write(msg)
                        
                        self.__RunTest(Config.Update_Temp_Module_Address)

                        if not os.path.exists(Config.TestMeVersionFolder):
                                os.mkdir(Config.TestMeVersionFolder)

                        LastInstalledVersion = ''
                        Updated_WAWi_AQC_Lib_Directory = Config.WAWi_AQC_Lib_Directory.replace('\\', '/')   
                        
                        FindInstalledVersionList = os.listdir(Updated_WAWi_AQC_Lib_Directory)
                        for elem in FindInstalledVersionList:
                                if len(os.listdir(Updated_WAWi_AQC_Lib_Directory + '/' + elem)) == 0:
                                        LastInstalledVersion = Updated_WAWi_AQC_Lib_Directory + '/' + elem
                                             
                        if not os.path.exists(Updated_WAWi_AQC_Lib_Directory + '/' + Config.SetupVersion):
                                os.mkdir(Updated_WAWi_AQC_Lib_Directory + '/' + Config.SetupVersion)
                        
                        self.__CopyFiles(Config.WAWi_AQC_Directory_Script, LastInstalledVersion, IsCopy = Config.IsCopyOfAQCOflatzeVersion)
                        self.__CopyFiles(Config.WAWi_AQC_Directory_NameMapping, LastInstalledVersion, ['Images'], IsCopy = Config.IsCopyOfAQCOflatzeVersion)

                        if Config.IsCreateBackUpOfNeueVersion:
                                Temp = mDBOperation.cDBOperation()                       
                                Temp.DBC('DB_TestMeBackup', SQLHost = Config.SQLHost)    
                                Delay(4820)
                        
                        NoCopy = os.listdir(Config.WAWiInstallAdress)
                        NoCopy = [ elem for elem in NoCopy if elem [:2].lstrip() == '1.']
                        
                        self.__CopyFiles(Config.WAWiInstallAdress, Config.TestMeVersionFolder, NoCopy, IsCopy = Config.IsBackUpOfWAWiAlteVersion)
                        
                except Exception as exp:
                    Log.Warning("UpdateMe: " + str(exp))                                                
#--
#...
#--      
        def __TodysJobs(self):
    
                try:

                        from datetime import datetime as date
                        WeekDay = date.today().strftime("%A")                                                                                                                              
                                
                        if WeekDay == 'Monday':
                                WeekDay = 'Montag'
                                
                        elif WeekDay == 'Tuesday':
                                WeekDay = 'Dienstag'
                                
                        elif WeekDay == 'Wednesday':
                                WeekDay = 'Mittwoch'
                                
                        elif WeekDay == 'Thursday':
                                WeekDay = 'Donnerstag'
                                
                        elif WeekDay == 'Friday':
                                WeekDay = 'Freitag'
                                
                        elif WeekDay == 'Saturday':
                                WeekDay = 'Samstag'

                        elif WeekDay == 'Sunday':
                                WeekDay = 'Sonntag'
                        
                        if WeekDay != self.Today:
                                self.Today = WeekDay
                                Temp = mDBOperation.cDBOperation()
                                Temp.DBC(Type = 'Command', SQLCommand = "USE AQC;EXEC spSERVERJOBs", SQLHost = Config.AQCHost)   
                
                except Exception as exp:
                    Log.Warning("TodysJobs: " + str(exp))                                          
#--
#...
#--
        def __FetchCommand(self):
    
                try:
                
                        self.Absender = Config.Default_Sender_Address
                
                        email_user = Config.TC_Address
                        email_pass = Config.TC_Password
                        M = imaplib.IMAP4(Config.TC_MailServer)
                        M.login(email_user, email_pass)

                        M.select('INBOX', readonly=True)

                
                        typ, msg_data = M.fetch(self.CommandTurn, '(BODY.PEEK[HEADER])')
                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                Header = response_part[1].decode("utf-8")
                                result = Header.find('<') + 1
                                Header = Header[result:]
                                result = Header.find('>')
                                self.Absender = Header[0:result]
                
                
                        typ, msg_data = M.fetch(self.CommandTurn, '(BODY.PEEK[TEXT])')
                        
                        for response_part in msg_data:
                                if isinstance(response_part, tuple): 
                                        msg = response_part[1].decode("utf-8") 
                                        self.__LogMsg(msg, self.Absender)
                                        msg = self.__DecodeMessage(msg)                        
                                        self.__LogMsg(msg, self.Absender)
                                        aqFile.WriteToTextFile(Config.Email_Decodec_Commands_Module_Address, msg, aqFile.ctANSI, True)
                                
                        M.close()
                        M.logout()
                        M = None
            
                except Exception as exp:
                    Log.Warning("FetchCommand: " + str(exp))
#--
#...
#--
        def __RunTest(self, filepath = Config.Email_Decodec_Commands_Module_Address, Commands = 'Start'):
    
                    try:
                    
                            Cmd = None

                            MName,FileExt = os.path.splitext(os.path.split(filepath)[-1])

                            if FileExt.lower() == '.py':
                                mPy = imp.load_source(MName, filepath)

                            if hasattr(mPy, Commands):
                                Cmd = getattr(mPy, Commands)()

                    except Exception as exp:
                            Log.Warning("RunTest: " + str(exp))
#--
#...
#--          
        def __RefreshCommand(self):
    
                try:
    
                        email_user = Config.TC_Address
                        email_pass = Config.TC_Password
                        M = imaplib.IMAP4(Config.TC_MailServer)
                        M.login(email_user, email_pass)

                        M.select('INBOX')

                        M.store(self.CommandTurn, '+FLAGS', r'(\Deleted)')
                
                        M.expunge()
                        
                        M.close()
                        M.logout()
                        M = None
            
                        if os.path.isfile(Config.Recorder_FullAddress):
                                os.remove(Config.Recorder_FullAddress)
                        
                except Exception as exp:
                    Log.Warning("RefreshCommand: " + str(exp))                     
#--
#...
#--
        def __DecodeMessage(self, Msg):
                
                try:
        
                        PrefixCommand = ''
                        PostFixCommand = ''
                        FunctionSrting = '#' + str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")) + '\n#Host: ' + socket.gethostname() + '\n#IP: '+ socket.gethostbyname(socket.gethostname()) + '\n\n' + '\ndef Start():\n'
                        CommandString = ''
                        
                        ExternalProcidure = []
                        
                        IsRestoreDB = False
                        IsDelete = 'True'
                        DBtoRestore = ''
                
                        result = Msg.find('#') + 1
                        Msg = Msg[result:]
                        result = Msg.find('#')
                        Msg = Msg[0:result]
                                
                        Msg = Msg.replace("=3D", "=")

                        Msg = Msg.split('\n')            
                
                        for Command in Msg:
                                if Command[0:1] == '$':
                                        Command = '\n' + 4*'\t' + 'Test = None\n' + 4*'\t' + 'import m' + Command[1:] + '\n' + 4* '\t' + 'Test = m' + Command[1:].rstrip() + '.c' + Command[1:].rstrip() + '()\n'
                                        CommandString = CommandString + Command
                                
                                elif Command[0:1] == '^':
                                        Command = 4*'\t' + 'Test.' + Command[1:].rstrip() + '\n'
                                        CommandString = CommandString + Command
                                
                                elif Command[0:1] == '~':
                                        Command = 4*'\t' + 'Test.' + Command[1:].rstrip() + '()\n'
                                        CommandString = CommandString + Command
                                                                
                                elif Command[0:1] == '&':
                                        Command = Command[1:].rstrip()
                                        Command = Command.replace(' ', '')
                                        
                                        Index = Command.find(', ')
                                        
                                        if Index <= 0:
                                                Index = len(Command)  
                                                 
                                        VersionLen = len(Command[0:Index])
                                        Version = Command[0:VersionLen] 
                                        Ordner = Command[Index + 1:]
                                        self.__VersionCommand(Version, Ordner)
                                                
                                elif Command[0:1] == '%':
                                        Command = Command[1:].rstrip()
                                        Command = Command.replace(' ', '')
                                        Index = Command.find(', ')
                                        
                                        if Index <= 0:
                                                Index = len(Command)                                         
                                        
                                        IsDelete = Command[Index + 1:]
                                        if IsDelete not in('True', 'False'):
                                                IsDelete = 'True'

                                        DBtoRestore = Command[:Index]
                                        IsRestoreDB = True
                                
                                elif Command[0:1] == '?':
                                        Command = Command[1:].rstrip()
                                        Command = Command.replace(' ', '')
                                        
                                        Index = Command.find(', ')
                                        StartJob = Command[:Index]
                                        self.JObString.append(StartJob)

                                        Command = Command[Index + 1:].rstrip()
                                        Index = Command.find(', ')
                                        EndJob = Command[:Index]
                                        self.JObString.append(EndJob)
                                
                                        Command = Command[Index + 1:].rstrip()
                                        Index = Command.find(', ')
                                        TagJob = Command[:Index]
                                        self.JObString.append(TagJob)
                                
                                        ZeitJob = Command[Index + 1:].rstrip()
                                        self.JObString.append(ZeitJob)
                                
                                        self.IsRun = False
                                        
                                elif Command[0:1] == '>':
                                        UpdateLen = len(Command[1:]) 
                                        Config.SetupVersion = Command[1:UpdateLen]
                                        hrfIndex = Config.SetupVersion.find('<')
                                        if hrfIndex >= 0:
                                                Config.SetupVersion = Config.SetupVersion[:hrfIndex]
                                        self.UpdateMe()
                                        self.IsRun = False                                        
                                
                                #External Resource Name
                                elif Command[0:1] == '!':
                                
                                        Command = Command[1:].rstrip()
                                        Prj = Command
                                        
                                        try:
                                                it = Config.ValidExternalResource.index(Prj)
                                        except Exception as exp:
                                                Log.Warning("Prj is not in ValidExternalResource" + str(exp))
                                                break
                                        finally:
                                                pass                                          
                                        
                                #External Resource Command
                                elif Command[0:1] == '-':
                                        Command = Command[1:].rstrip()
                                        ExternalProcidure.append(Command)
                                        
                                        Config.IsInExternalMode = True

                                        
                                        
                        if len(ExternalProcidure) > 0:    
                                Command = '\n' + 2*'\t' + 'from AQC.Setting.TestApp import Config' + '\n'
                                Command = Command + 2*'\t' + 'import os' + '\n'
                                        
                                Command = Command + 2*'\t' + 'import mServer' + '\n\n'
                                Command = Command + 2*'\t' + 'Server = mServer.Server()' + '\n'
                                
                                tempProcArray = '['
                                
                                for it in ExternalProcidure:
                                        tempProcArray = tempProcArray + '\'' + it + '\', '
                                
                                tempProcArray = tempProcArray[:len(tempProcArray) - 2] + ']'
                                
                                if IsRestoreDB:
                                        Command = Command + 2*'\t' + 'Server.EnterExternalProjektMode(Prj = \'' + Prj + '\', Proc = ' + tempProcArray + ', Empfanger = \'' + self.Absender + '\', DBtoRestore = \'' + DBtoRestore + '\', IsDelete = ' + IsDelete + ')\n\n'
                                else:
                                        Command = Command + 2*'\t' + 'Server.EnterExternalProjektMode(Prj = \'' + Prj + '\', Proc = ' + tempProcArray + ', Empfanger = \'' + self.Absender + '\')\n\n'
                                        
                                Command = Command + 2*'\t' + 'os.startfile(Config.ChangeProjectBat)' + '\n'
                                CommandString = CommandString + Command

                        else:
                                if IsRestoreDB:
                                        self.ftpOperations(DBtoRestore, IsDelete, Methode = 'Download')

                        if not Config.IsInExternalMode:
                                PrefixCommand_0 = '\n' + 2*'\t' + 'Test = None\n' + 2*'\t' + 'import mWAWi' +'\n' + 2* '\t' + 'Test = mWAWi.cWAWi()\n' + 2* '\t' + 'Test.RunWAWi()\n'
                                PrefixCommand_1 = '\n' + 2*'\t' + 'Test = None\n' + 2*'\t' + 'import mRecorder' +'\n' + 2* '\t' + 'Test = mRecorder.cRecorder()\n' + 2* '\t' + 'Test.StartRecord()\n'
                                PrefixCommand_2 = '\n' + 2*'\t' + 'try:\n'
                                
                                PostFixCommand__ = '\n' + 2*'\t' + 'except Exception as exp:\n' + 4*'\t' + 'Log.Warning("DecodeMessage Falsche Module: " + str(exp))\n'
                                PostFixCommand_0 = '\n' + 2*'\t' + 'Test = None\n' + 2*'\t' + 'import mRecorder' + '\n' + 2* '\t' + 'Test = mRecorder.cRecorder()\n' + 2* '\t' + 'Test.StopRecord()\n'
                                PostFixCommand_1 = '\n' + 2*'\t' + 'Test = None\n' + 2*'\t' + 'import mWAWi' +'\n' + 2* '\t' + 'Test = mWAWi.cWAWi()\n' + 2* '\t' + 'Test.ShutdownWAWi()\n'
                                PostFixCommand_2 = '\n' + 2*'\t' + 'Test.Ergebnisprotokoll()\n'
                                
                        else:
                                PrefixCommand_0 = ''
                                PrefixCommand_1 = ''
                                PrefixCommand_2 = ''
                                            
                                PostFixCommand__ = ''
                                PostFixCommand_0 = ''
                                PostFixCommand_1 = ''
                                PostFixCommand_2 = ''
                                
                        PrefixCommand = PrefixCommand_0 + PrefixCommand_1 + PrefixCommand_2
                        PostFixCommand = PostFixCommand__ + PostFixCommand_0 + PostFixCommand_1 + PostFixCommand_2
                        CommandString = FunctionSrting + PrefixCommand + CommandString + PostFixCommand
                        
                        return CommandString
        
                except Exception as exp:
                        Log.Warning("DecodeMessage: " + str(exp))
#--
#...
#--
        def __VersionCommand(self, Version, Ordner = ''):
                
                try:
                
                        self.__DownloadWAWiForSetup(Version, Ordner)
        
                        if os.path.exists(Config.WAWiSetup):
                                os.remove(Config.WAWiSetup)
                        
                        Temp = mWAWiSetup.cWAWiSetup()
                        Temp.InstallWAWi()                                        

                except Exception as exp:
                        Log.Warning("VersionCommand: " + str(exp))
#--
#...
#--
        def __LogMsg(self, msg, Sender):
                
                try:


                        file = open(Config.ServerLog_Address, 'a')
                        LogToWreit = 210*'-' + '\n'
                        LogToWreit = 'From: ' + Sender + '\n' + 'Eingang befahl am ' + str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")) + '\nDas Host: ' + Config.TestPlatforms + '\n\n' + msg + '\n\n' + LogToWreit
                        file.write(LogToWreit)
                        file.close()
                
                        if self.IsRun != True:
                                LogToWreit = LogToWreit.replace('"', '')
                                LogToWreit = LogToWreit.replace("'", "''")
                                tempIndex = LogToWreit.find('--')
                                LogToWreit = LogToWreit[:tempIndex]

                                LogToWreit = "'" + LogToWreit + "'"
                                
                                SQLCommand = 'USE AQC;INSERT INTO [SERVERJOBS] ([Job], [StartJob], [EndJob], [Tag], [RunTime]) VALUES (' + LogToWreit + ', ' + "'" + self.JObString[0]  + "'" + ', ' + "'" + self.JObString[1] + "'" + ', ' + "'" + self.JObString[2] + "'" + ', ' + "'" + self.JObString[3] + "'" +' )'
                                Temp = mDBOperation.cDBOperation()
                                Temp.DBC(SQLCommand = SQLCommand, SQLHost = Config.AQCHost)
                                self.JObString.clear()

                                
                except Exception as exp:
                        Log.Warning("LogMsg: " + str(exp))     
#--
#...
#--                              
        def ftpOperations(self, DBName = '', IsDelete = '', Methode = 'Download', ListFileDirctoryOfSourceForUpload = [[Config.TestAppFolder]], DirectoryOfDistination = ''):
    
                try:
    
                        if not isinstance(IsDelete, bool):
                                if IsDelete == 'True':
                                        IsDelete = True
                                else:
                                        IsDelete = False
                                
                        ftp_user = Config.ftp_User
                        ftp_pass = Config.ftp_Password
                
                        M = FTP_TLS(Config.ftp_Server, timeout=70000)
                        M.login(ftp_user, ftp_pass)
                
                        FileForFTP = DBName +'.bak'
                        
                        if Methode == 'Download':
                                M.set_pasv(True)
                                M.cwd(Config.ftp_MailsDB_Address)
                                wdir = M.sendcmd('PWD')
                
                                
                                DownloadFile = open(Config.DB_ToRestore, 'wb')
                
                                M.retrbinary("RETR " + FileForFTP, DownloadFile.write, 8 * 1024)
                
                                DownloadFile.close()
                
                                Temp = mDBOperation.cDBOperation()
                                Temp.DBC('MailRestore', SQLHost = Config.SQLHost)

                                if bool(IsDelete):
                                        M.delete(FileForFTP)
                                    
                                os.remove(Config.DB_ToRestore)
                                
                        elif Methode == 'Upload':
                                file = open(ListFileDirctoryOfSourceForUpload[0, 0]  + '\\' +  FileForFTP, 'rb')
                                M.storbinary('STOR '+ FileForFTP, file)
                                file.close()
                                

                        elif Methode == 'UploadWithCreateDirectory':
                        
                                filelist = []
                                M.cwd('/Test-Result')
                                
                                M.retrlines('LIST', filelist.append)
                                for f in filelist:
                                        if f.split()[-1] == DirectoryOfDistination and f.upper().startswith('D'):
                                                self.__ftpRemoveDirectory(M, DirectoryOfDistination)  
                        
                                M.mkd(DirectoryOfDistination)
                                M.cwd(DirectoryOfDistination)
                                
                                for file in ListFileDirctoryOfSourceForUpload:
                                        FileToUpload = open(file[0] + '\\' + file[1], 'rb')
                                        M.storbinary('STOR '+ file[1], FileToUpload)
                                        FileToUpload.close()
                                
                        M.quit()
                                
                except Exception as exp:
                    Log.Warning("ftpOperations " + str(exp))    
                    M.quit()
                    DownloadFile.close()
#--
#...
#--
        def __ftpRemoveDirectory(self, M, path):
                try:
                        M.delete(path)
                except:
                        try:
                                M.rmd(path)
                        except:
                                if M.pwd()=="/":
                                        M.cwd(M.pwd()+path)
                                else:
                                        M.cwd(M.pwd()+"/"+path)
            
                                dirs=M.nlst()
                                for di in dirs:
                                        self.__ftpRemoveDirectory(M,di)
                                if M.pwd()=="/":
                                        pass
                                else:
                                        M.cwd("..")
                                        M.rmd(path)
##--
##...
##--            
#        def __ftpCopyFolder(self, M, src, dest):
#            
#                try:
#
#                        for item in os.listdir(src):
#                                file_path = os.path.join(src, item)
#                                file_path = file_path.replace('\\', '/') 
#
#                                if os.path.isfile(file_path):
#                                        M.cwd(dest)                   
#                                                             
#                                        file = open(src, 'rb')
#                                        M.storbinary('STOR '+ src + '\\' + file_path, file)
#                                        file.close()
#                                
#                                
#                                elif os.path.isdir(file_path):
#                                        new_dest = os.path.join(dest, item)
#                                        new_dest = new_dest.replace('\\', '/')
#                                        
#                                        if not os.path.isdir(new_dest):
#                                                M.cwd(dest)
#                                                M.mkd(item)
#                                                
#                                        self.__ftpCopyFolder(M, file_path, new_dest)
#                                                
#                except Exception as exp:
#                    Log.Warning("__ftpCopyFolder: " + str(exp))
#--
#...
#--
        def __DownloadWAWiForSetup(self, FileName = '', Ordner = '', IsGetListOfWAWiVersion = False, Attempt = 5):
    
                try:
    
                        username = Config.WAWiRepo_Username
                        password = Config.WAWiRepo_Password
                        baseurl = Config.WAWiRepo_baseurl

                        import http.client
                        http.client.HTTPConnection._http_vsn = 10
                        http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'                        
                                                
                        if Ordner != '':
                                Config.WAWiRepo_Ordner = Ordner

                        PYTHONHTTPSVERIFY=0
                                
                        manager = request.HTTPPasswordMgrWithDefaultRealm()
                        manager.add_password(None, baseurl, username, password)

                        auth = request.HTTPBasicAuthHandler(manager)

                        opener = request.build_opener(auth)
                        request.install_opener(opener)

                        if IsGetListOfWAWiVersion:

                                IsFehlerImVerbinung = True
                                TimeOut = 1000000
                                
                                while IsFehlerImVerbinung:
                                
                                        try:

                                                response = request.urlopen(baseurl + Config.WAWiRepo_Ordner, timeout = TimeOut)
                                                IsFehlerImVerbinung = False
                                                break

                                        except Exception as exp:
                                            Log.Warning("__DownloadWAWiTimeOut " + str(exp))
                                            Delay(9861)
                                        
                                if Config.IsSetupWAWiHasFehler:
                                        WAWiPage = response.read().decode("utf-8").split('<a href=')[-2]
                                        Config.IsSetupWAWiHasFehler = False
                                else:
                                        WAWiPage = response.read().decode("utf-8").split('<a href=')[-1]
                                
                                LastWAWiVersion = WAWiPage[1 : WAWiPage.find('>') - 1]
                                return LastWAWiVersion
                                
                        else:
                                                
                                while os.path.exists(Config.WAWiSetup):
                                        os.remove(Config.WAWiSetup)
                                        Delay(5150)

                                while not os.path.exists(Config.WAWiSetup) or Attempt < 0 :
                                        response = request.urlopen(baseurl + Config.WAWiRepo_Ordner + FileName)        
                                        Download = response.read()
                                                        
                                        with open(Config.WAWiSetup , "wb") as code:
                                            code.write(Download)
                                            
                                        Delay(5150)
                                        Attempt = Attempt - 1
                            
                except Exception as exp:
                    Log.Warning("__DownloadWAWiForSetup " + str(exp))
#--
#...
#--            
        def __CopyFiles(self, src, dest, NoCopy = [''], IsCopy = True):
            
                try:

                        if not IsCopy:
                                return
                               
                        NoCopyFlag = False
                        
                        for item in os.listdir(src):
                                file_path = os.path.join(src, item)
                                file_path = file_path.replace('\\', '/') 

                                if os.path.isfile(file_path):
                                        for elem in NoCopy:
                                                if elem == file_path:
                                                        NoCopyFlag = True
                                                        
                                        if not NoCopyFlag:
                                                shutil.copy(file_path, dest)
                                
                                
                                elif os.path.isdir(file_path):
                                        new_dest = os.path.join(dest, item)
                                        new_dest = new_dest.replace('\\', '/')
                                        for elem in NoCopy:
                                                if elem == item:
                                                        NoCopyFlag = True
                                        
                                        if not NoCopyFlag:
                                                if not os.path.isdir(new_dest):
                                                        os.mkdir(new_dest)
                                                self.__CopyFiles(file_path, new_dest, NoCopy)
                                                
                                NoCopyFlag = False
                            
                except Exception as exp:
                    Log.Warning("__CopyFiles " + str(exp))                                             
#--
#...
#--            
        def __TestExecuteDeleteExtraFiles(self):
            
                try:
                
                        if os.path.exists(Config.WindowTempFolder):
                                for SubDirectory in os.listdir(Config.WindowTempFolder):
                                        if os.path.isdir(Config.WindowTempFolder + '/' + SubDirectory):
                                                if os.access(Config.WindowTempFolder + '/' + SubDirectory, os.F_OK):
                                                
                                                        try:
                                        
                                                                shutil.rmtree(Config.WindowTempFolder + '/' + SubDirectory)
                                        
                                                        except Exception as exp:
                                                                Log.Message('__TestExecuteDeleteExtraFiles, One file s for other process')
                                        
                                                        finally:
                                                                pass
                                        else:
                                        
                                                try:
                                
                                                        os.remove(Config.WindowTempFolder + '/' + SubDirectory)
                                        
                                                except Exception as exp:
                                                        Log.Message('__TestExecuteDeleteExtraFiles, One file s for other process')
                                        
                                                finally:
                                                        pass
                            
                except Exception as exp:
                    Log.Warning("__TestExecuteDeleteExtraFiles " + str(exp))  
#--
#...
#--            
        def EnterExternalProjektMode(self, Prj, Proc, DBtoRestore = '', IsDelete = 'True', Empfanger = ''):
            
                try:

                        Temp = mDBOperation.cDBOperation()
                        Temp.DBC(Type = 'Command', SQLCommand = "USE AQC;UPDATE Config SET [Value] = \'True\' WHERE Config = \'IsInExternalMode\'", SQLHost = Config.AQCHost)
                        
                        if Empfanger == '':
                                Empfanger = self.Absender
                        
                        Commands = ''
                        nmServer = Config.WAWi_AQC_Directory_NameMapping
                        taServer = Config.WAWi_AQC_Directory_TestedApps
                        stServer = Config.WAWi_AQC_Directory_Stores                           
                        ktServer = Config.WAWi_AQC_Directory_KeywordTests
                        mdServer = Config.WAWi_AQC_Directory_Mds
                        pjServer = Config.WAWi_AQC_Directory_Projekt
                        
                        TestUmgebung = Config.WAWi_AQC_Directory_Script + r'\TestUmgebung.py'
                        
                        masterTemp = Config.Temp_Directory + r'\master'
                        clientTemp = Config.Temp_Directory + r'\client'
                        stTemp = Config.Temp_Directory + r'\STs'
                        spTemp = Config.Temp_Directory + r'\SPs'
                        ktTemp = Config.Temp_Directory + r'\KTs'
                        mdTemp = Config.Temp_Directory + r'\MDs'

                        if Prj == 'Codebuster_0':
                                nmExtrnal = Config.Codebuster_0 + r'\NameMapping'
                                taExtrnal = Config.Codebuster_0 + r'\TestedApps'
                                stExtrnal = Config.Codebuster_0 + r'\Stores'
                                ktExtrnal = Config.Codebuster_0 + r'\KeywordTests'
                                mdExtrnal = Config.Codebuster_0
                                
                        else:
                                return                     
                              
                        self.__SetTestPlattform()  
                                
                        if Config.TestPlatforms == 'TC':
                                Platform = 'TestComplete.exe'
                                RunAddressCommand = 'CD ' + Config.TestCompleteExecAdress +' \n'
                                DirectoryMdsCommand = 'start \"\" TestComplete.exe ' + '"' + Config.WAWi_AQC_Directory_Mds + '"' + ' /run\n'
                                
                        elif Config.TestPlatforms == 'TE':
                                Platform = 'TestExecute.exe'
                                RunAddressCommand = 'CD ' + Config.TestExecuteExecAdress +' \n'
                                DirectoryMdsCommand = 'start \"\" TestExecute.exe ' + '"' + Config.WAWi_AQC_Directory_Mds + '"' + ' /run\n'                                
                        
                        Commands = Commands + '@echo off\n'
                        Commands = Commands + 'REM Clears the screen\nCLS\ntaskkill /f /im \"' + Platform + '\" \n'
                        
                        Commands = Commands + 'echo V| xcopy /y/v ' + mdServer + ' ' + masterTemp + ' >NUL\n'
                        Commands = Commands + 'echo V| xcopy /y/v ' + mdExtrnal + ' ' + clientTemp + ' >NUL\n'

                        Commands = Commands + 'CLS\n'
                        Commands = Commands + 'TIMEOUT 5\n'
                        
                        KeyWords = ''
                        KeyWordAddress = ' -k ' + ktExtrnal + r'\KeywordTests.tcKDT'
                        MdsAddress = ' -m ' + mdExtrnal + r'\WAWi.mds'
                        EexcutionPlanAddress = ' -p ' + mdExtrnal + r'\EexcutionPlan.txt'
                        
                        for it in Proc:
                                KeyWords = KeyWords + ' -a ' + it
                                
                        Commands = Commands + r'C:\OneDrive\ExternalResources\Manager\UpdateMdsProjekt.exe' + KeyWords + KeyWordAddress + MdsAddress + EexcutionPlanAddress + ' \n'
                        
                        Commands = Commands + 'CLS\n'
                        Commands = Commands + 'TIMEOUT 5\n'

                        Commands = Commands + 'DEL /f/q ' + mdServer + '\n'

                        Commands = Commands + 'CLS\n'
                        Commands = Commands + 'TIMEOUT 1\n'
                        Commands = Commands + 'echo v| copy /y/v ' + mdExtrnal + ' ' + pjServer + ' >NUL\n'

                        Commands = Commands + 'CLS\n'
                        Commands = Commands + 'CD C:\\ \n'
                        
                        Commands = Commands + 'CLS\n'
                        Commands = Commands + 'TIMEOUT 3\n'
                        Commands = Commands + RunAddressCommand
                        Commands = Commands + 'CLS\n'
                        Commands = Commands + 'TIMEOUT 5\n'                        
                        Commands = Commands + DirectoryMdsCommand
                        Commands = Commands + 'CLS\n'
                        Commands = Commands + 'TIMEOUT 5\n'
                        Commands = Commands + 'EXIT'
                        
                        if os.path.exists(Config.ChangeProjectCodesBat):
                                os.remove(Config.ChangeProjectCodesBat)                                       
                                
                        TempFile = open(Config.ChangeProjectCodesBat, 'a')
                        TempFile.write(Commands)
                        TempFile.close()                       
                        
                        if os.path.exists(TestUmgebung):
                                os.remove(TestUmgebung)                            
                                
                        Commands = ''
                       
                        Commands = Commands + '\ndef Start():\n'
                        Commands = Commands + 2*'\t' + 'from AQC.Setting.TestApp import Config, os\n'
                        Commands = Commands + 2*'\t' + 'Config.IsInExternalMode = True\n\n'
                        Commands = Commands + 2*'\t' + 'Log.Enabled = False\n\n'
                        
                        Commands = Commands + 2*'\t' + 'try:\n\n'
                        Commands = Commands + 4*'\t' + 'OS_Proc_List = os.popen(\'tasklist\').read().strip().split(\'\\n\')\n\n'
                        Commands = Commands + 4*'\t' + 'for it in OS_Proc_List:\n'
                        Commands = Commands + 6*'\t' + 'if it.find(\'JTL-Wawi.exe\') == 0:\n'
                        Commands = Commands + 8*'\t' + 'os.system(\"TASKKILL /F /IM JTL-Wawi.exe\")\n'
                        Commands = Commands + 8*'\t' + 'Delay(5000)\n'
                        Commands = Commands + 8*'\t' + 'break\n\n'
                        Commands = Commands + 2*'\t' + 'except Exception as exp:\n' + 4*'\t' + 'Log.Warning("xmExternal_DBtoRestore: " + str(exp))\n\n'
                        
                        if DBtoRestore != '':
                                Commands = Commands + 2*'\t' + 'try:\n\n'
                                Commands = Commands + 4*'\t' + 'import mServer\n\n'
                                Commands = Commands + 4*'\t' + 'Server = mServer.Server()\n\n'
                                Commands = Commands + 4*'\t' + 'Server.ftpOperations(\'' + DBtoRestore + '\', ' + str(IsDelete) + ')\n\n'                               
                                Commands = Commands + 2*'\t' + 'except Exception as exp:\n' + 4*'\t' + 'Log.Warning("xmExternal_DBtoRestore: " + str(exp))\n\n'

                        Commands = Commands + 2*'\t' + 'try:\n'                                                                                
                        Commands = Commands + '\n' + 4*'\t' + 'Test = None\n' + 4*'\t' + 'import mRecorder' + '\n' + 4* '\t' + 'Test = mRecorder.cRecorder()\n' + 4* '\t' + 'Test.StartRecord()\n\n'
                        Commands = Commands + 2*'\t' + 'except Exception as exp:\n' + 4*'\t' + 'Log.Warning("xmExternal_Start_Recorder: " + str(exp))\n\n'
                        
                        Commands = Commands + '\ndef Stop():\n\n'
                        Commands = Commands + 2*'\t' + 'try:\n'
                        Commands = Commands + '\n' + 4*'\t' + 'Test = None\n' + 4*'\t' + 'import mRecorder' + '\n' + 4* '\t' + 'Test = mRecorder.cRecorder()\n' + 4* '\t' + 'Test.StopRecord()\n\n'
                        Commands = Commands + 2*'\t' + 'except Exception as exp:\n' + 4*'\t' + 'Log.Warning("xmExternal_Stop_Recorder: " + str(exp))\n\n'
                        
                        Commands = Commands + 2*'\t' + 'try:\n'
                        Commands = Commands + '\n' + 4*'\t' +'import mServer\n\n' 
                        Commands = Commands + 4*'\t' + 'Server = mServer.Server()\n'
                        Commands = Commands + 4*'\t' + 'Server.SendResultMailInExternalProjektMode( Empfanger = \'' + Empfanger + '\')\n'
                        Commands = Commands + 4*'\t' + 'Server.ExitExternalProjektMode(\'' + Prj + '\')\n\n'
                        Commands = Commands + 2*'\t' + 'except Exception as exp:\n' + 4*'\t' + 'Log.Warning("xmExternal_Stop_Server: " + str(exp))\n\n'
                        
                        TempFile = open(TestUmgebung, 'a')
                        TempFile.write(Commands)
                        TempFile.close()       
                        
                except Exception as exp:
                    Log.Warning("ExternalProjekt: " + str(exp))                     
#--
#...
#--            
        def ExitExternalProjektMode(self, Prj):
            
                try:
                                
                        Commands = ''
                        nmServer = Config.WAWi_AQC_Directory_NameMapping
                        taServer = Config.WAWi_AQC_Directory_TestedApps
                        stServer = Config.WAWi_AQC_Directory_Stores
                        ktServer = Config.WAWi_AQC_Directory_KeywordTests
                        mdServer = Config.WAWi_AQC_Directory_Mds
                        pjServer = Config.WAWi_AQC_Directory_Projekt
                        
                        TestUmgebung = Config.WAWi_AQC_Directory_Script + r'\TestUmgebung.py'
                        excutionPlanAddress = mdServer + r'\EexcutionPlan.txt'
                        
                        Temp = Config.Temp_Directory
                        masterTemp = Config.Temp_Directory + r'\master'
                        clientTemp = Config.Temp_Directory + r'\client'
                        stTemp = Config.Temp_Directory + r'\STs'
                        ktTemp = Config.Temp_Directory + r'\KTs'
                        mdTemp = Config.Temp_Directory + r'\MDs'
                        
                        if Prj == 'Codebuster_0':
                                nmExtrnal = Config.Codebuster_0 + r'\NameMapping'
                                taExtrnal = Config.Codebuster_0 + r'\TestedApps'
                                stExtrnal = Config.Codebuster_0 + r'\Stores'
                                ktExtrnal = Config.Codebuster_0 + r'\KeywordTests'
                                mdExtrnal = Config.Codebuster_0
                                
                        else:
                                return

                                
                        self.__SetTestPlattform()
                        
                        if Config.TestPlatforms == 'TC':
                                Platform = 'TestComplete.exe'
                                RunAddressCommand = 'CD ' + Config.TestCompleteExecAdress +' \n'
                                DirectoryMdsCommand = 'start \"\" TestComplete.exe ' + '"' + Config.WAWi_AQC_Directory_Mds + '"' + ' /run\n'
                                
                        elif Config.TestPlatforms == 'TE':
                                Platform = 'TestExecute.exe'
                                RunAddressCommand = 'CD ' + Config.TestExecuteExecAdress +' \n'
                                DirectoryMdsCommand = 'start \"\" TestExecute.exe ' + '"' + Config.WAWi_AQC_Directory_Mds + '"' + ' /run\n'
   
                        Commands = Commands + '@echo off\n'
                        Commands = Commands + 'CLS\n'
                        Commands = Commands + 'REM Clears the screen\nCLS\ntaskkill /f /im \"' + Platform + '\" \n'
                        
                        Commands = Commands + 'CLS\n'
                        Commands = Commands + 'TIMEOUT 10\n'
                        Commands = Commands + 'DEL /f/q ' + mdServer + ' >NUL\n'
                        Commands = Commands + 'DEL /f/q ' + excutionPlanAddress + ' >NUL\n'
                        
                        Commands = Commands + 'CLS\n'
                        Commands = Commands + 'TIMEOUT 1\n'
                        
                        Commands = Commands + 'echo V| xcopy /y/v ' + masterTemp + ' ' + pjServer + ' >NUL\n'
                        Commands = Commands + 'echo V| xcopy /y/v ' + clientTemp + ' ' + mdExtrnal + ' >NUL\n'
                        #Commands = Commands + 'echo V| xcopy /y/v ' + mdTemp + ' ' + pjServer + ' >NUL\n'
                        
                        Commands = Commands + 'CLS\n'
                        Commands = Commands + 'TIMEOUT 5\n'
                        
                        Commands = Commands + 'RMDIR /S/Q ' + Temp + ' >NUL\n'
                        Commands = Commands + 'CD C:\\ \n'
                        
                        Commands = Commands + 'CLS\n'
                        Commands = Commands + 'TIMEOUT 1\n'
                        Commands = Commands + RunAddressCommand
                        
                        Commands = Commands + 'CLS\n'
                        Commands = Commands + 'TIMEOUT 1\n'
                        Commands = Commands + DirectoryMdsCommand
                        
                        Commands = Commands + 'CLS\n'
                        Commands = Commands + 'TIMEOUT 10\n'
                        Commands = Commands + 'EXIT'
                        
                        if os.path.exists(Config.ChangeProjectCodesBat):
                                os.remove(Config.ChangeProjectCodesBat)
                
                        TempFile = open(Config.ChangeProjectCodesBat, 'a')
                        TempFile.write(Commands)
                        TempFile.close()                      

                        if os.path.exists(TestUmgebung):
                                os.remove(TestUmgebung)                            
                                
                        Commands = ''
                        Commands = Commands + 'import mServer, Config\n\n' 
                        
                        Commands = Commands + '#--\n#...\n#--\n'
                        Commands = Commands + 'def Stop():\n'
                        Commands = Commands + 2*'\t' + 'pass\n'
                        
                        Commands = Commands + '#--\n#...\n#--\n'
                        Commands = Commands + 'def Start():\n'
                        
                        Commands = Commands + 2*'\t' + 'Config.IsInExternalMode = False\n'
                        Commands = Commands + 2*'\t' + 'Log.Enabled = False\n\n'
                        
                        Commands = Commands + 2*'\t' + 'Server = mServer.Server()\n'
                        Commands = Commands + 2*'\t' + 'Server.Start()\n'
                        
                        TempFile = open(TestUmgebung, 'a')
                        TempFile.write(Commands)
                        TempFile.close()                         

                        Temp = mDBOperation.cDBOperation()
                        Temp.DBC(Type = 'Command', SQLCommand = "USE AQC;UPDATE Config SET [Value] = \'False\' WHERE Config = \'IsInExternalMode\'", SQLHost = Config.AQCHost)
                        
                        os.startfile(Config.ChangeProjectBat)
                                                
                except Exception as exp:
                    Log.Warning("ExternalProjekt: " + str(exp))
#--
#...
#--
        def SendResultMailInExternalProjektMode(self, Empfanger):
                
                try:
                
                        subject = 'TestComplete, Your Command Result'
                        Body = 'HI'
                        HTML = """\<html></html>"""
                        
                        Node = os.environ['COMPUTERNAME']
                        User = os.getlogin()
                        
                        Body = '<h1>Hallo,</h1>\n<h3>Das Host: ' + Node + '\nDer Benutzer: ' + User + '\n\nwie gewunscht wird der von Dir angeforderte Testfall am ' + str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")) + ' getestet.\n\n</h3>\n\n<h2>Ihr TC-Team</h2>'
                        Body = Body.replace("\n", "<br>")
                        Body = Body.replace(" ", "&nbsp;")
                        
                        HTML = """\
                        <html>
                          <head>
                            <style>
                                    h1 {color:red;   padding: 10px;font-family: Arial;font-size: 80%;font-weight:lighter;}
                                    h2 {color:green; padding: 10px;font-family: Arial;font-size: 80%;}
                                    h3 {color:black; padding: 10px;font-family: Arial;font-size: 80%;font-weight:lighter;}
                                    p {color:blue;  padding: 10px;font-family: Lucida Console;font-size: 80%;}
                            </style>
                            </head>
                          
                            <body>
                            """ + Body  + """
                            </body>
                        </html>
                        """   
                                             
                        self.__EmailOperation(Empfanger, subject, Body, HTML, IsAttachVideo = Config.IsVideoAttached, IsTCLogAttached = Config.IsTCLogAttached, IseLogAttached = Config.IseLogAttached, IseLogExportToftp = Config.IseLogExportToftp)
        
                except Exception as exp:
                        Log.Warning("SendConfirmationEmail: " + str(exp))
#--
#...
#--
        def __SendUpdateInfo(self):
                
                try:
                        
                        subject = 'TestComplete, info für Update'
                        Body = 'HI'
                        HTML = """\<html></html>"""
                        
                        Node = os.environ['COMPUTERNAME']
                        User = os.getlogin()
                        
                        Body = '<h1>Hallo,</h1>\n<h3>im Host: ' + Node + '\nmit der Benutzer: ' + User + '\nich fange an, das WAWi am ' + str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")) + ' zur Version ' + Config.AktualVersion + ' zu aktualisieren.\n\n</h3>\n\n<h2>Ihr TC-Team</h2>'
                        Body = Body.replace("\n", "<br>")
                        Body = Body.replace(" ", "&nbsp;")
                        
                        HTML = """\
                        <html>
                          <head>
                            <style>
                                    h1 {color:red;   padding: 10px;font-family: Arial;font-size: 80%;font-weight:lighter;}
                                    h2 {color:green; padding: 10px;font-family: Arial;font-size: 80%;}
                                    h3 {color:black; padding: 10px;font-family: Arial;font-size: 80%;font-weight:lighter;}
                                    p {color:blue;  padding: 10px;font-family: Lucida Console;font-size: 80%;}
                            </style>
                            </head>
                          
                            <body>
                            """ + Body  + """
                            </body>
                        </html>
                        """   
                        
                        Empfanger = Config.Default_Dev_Address
                        Login = Config.TC_konfig_Address
                        Password = Config.TC_konfig_Password
                                             
                        self.__EmailOperation(Empfanger, subject, Body, HTML, login = Login, password = Password)
        
                except Exception as exp:
                        Log.Warning("SendUpdateInfo: " + str(exp))
#--
#...
#--
        def __SendRedirctAQCInfo(self):
                
                try:
                
                        subject = 'TestComplete, Create Lockal AQC'
                        Body = 'HI'
                        HTML = """\<html></html>"""
                        
                        Node = os.environ['COMPUTERNAME']
                        User = os.getlogin()
                        
                        Body = '<h1>Hallo,</h1>\nDas Host: ' + Node + '\nDer Benutzer: ' + User + '\n</h3>I have create local AQC-DB on ' + str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")) + '\n\n</h3>\n\n<h2>Ihr TC-Team</h2>'
                        Body = Body.replace("\n", "<br>")
                        Body = Body.replace(" ", "&nbsp;")
                        
                        HTML = """\
                        <html>
                          <head>
                            <style>
                                    h1 {color:red;   padding: 10px;font-family: Arial;font-size: 80%;font-weight:lighter;}
                                    h2 {color:green; padding: 10px;font-family: Arial;font-size: 80%;}
                                    h3 {color:black; padding: 10px;font-family: Arial;font-size: 80%;font-weight:lighter;}
                                    p {color:blue;  padding: 10px;font-family: Lucida Console;font-size: 80%;}
                            </style>
                            </head>
                          
                            <body>
                            """ + Body  + """
                            </body>
                        </html>
                        """   
                        
                        Empfanger = Config.Default_Dev_Address
                        Login = Config.TC_konfig_Address
                        Password = Config.TC_konfig_Password
                                             
                        self.__EmailOperation(Empfanger, subject, Body, HTML, login = Login, password = Password)
        
                except Exception as exp:
                        Log.Warning("SendRedirctAQCInfo: " + str(exp))
#--
#...
#--
        def __SendConfirmationEmail(self, Empfanger):
                
                try:
                
                        subject = 'TestComplete, Confirm Your Command'
                        Body = 'HI'
                        HTML = """\<html></html>"""
                        
                        Node = os.environ['COMPUTERNAME']
                        User = os.getlogin()
                        
                        Body = '<h1>Hallo,</h1>\nDas Host: ' + Node + '\nDer Benutzer: ' + User + '\n</h3>wie gewunscht wird der von Dir angeforderte Testfall von ' + str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")) + ' getestet.\n\nWir werden Dir das Ergebnis mitteilen.</h3>\n\n<h2>Ihr TC-Team</h2>'
                        Body = Body.replace("\n", "<br>")
                        Body = Body.replace(" ", "&nbsp;")
                        
                        HTML = """\
                        <html>
                          <head>
                            <style>
                                    h1 {color:red;   padding: 10px;font-family: Arial;font-size: 80%;font-weight:lighter;}
                                    h2 {color:green; padding: 10px;font-family: Arial;font-size: 80%;}
                                    h3 {color:black; padding: 10px;font-family: Arial;font-size: 80%;font-weight:lighter;}
                                    p {color:blue;  padding: 10px;font-family: Lucida Console;font-size: 80%;}
                            </style>
                            </head>
                          
                            <body>
                            """ + Body  + """
                            </body>
                        </html>
                        """   
                                             
                        self.__EmailOperation(Empfanger, subject, Body, HTML)                        
        
                except Exception as exp:
                        Log.Warning("__SendConfirmationEmail: " + str(exp))    
#--
#...
#--
        def __EmailOperation(self, Empfanger, subject, Body, HTML, IsAttachVideo = False, IsTCLogAttached = False, IseLogAttached = False, IseLogExportToftp = False, login = '', password = ''):
                
                try:
                
                        ListFileDirctoryOfSourceForUpload = [[]]
                                        
                        if login == '' or password == '':
                                login = Config.TC_Address
                                password = Config.TC_Password
                        smtpserver=Config.TC_MailServer_SMTP
                                       
                        message = MIMEMultipart('alternative')
                        message['subject'] = subject
                        message['From'] = login

                        Body =  MIMEText(Body, 'plain')
                        HTML = MIMEText(HTML, 'html')
                        
                        message.attach(Body)
                        message.attach(HTML)
                        
                        if IsAttachVideo:
                                File = os.listdir(Config.Recorder_Address)
                                if bool(File):
                                        filename = "Test.avi"
                                        
                                        if os.path.getsize(Config.Recorder_Address + r'\Test.avi')/1048576 < 13.5:
                                                attachment = open(Config.Recorder_Address + r'\Test.avi', "rb") 
                                                tempHolder = MIMEBase('application', 'octet-stream') 
                                                tempHolder.set_payload((attachment).read()) 
                                                encoders.encode_base64(tempHolder) 
                                                tempHolder.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
                                                message.attach(tempHolder)
                                        else:
                                                ListFileDirctoryOfSourceForUpload.append([Config.Recorder_Address, 'Test.avi'])
                                                
                                                                                
                        if IsTCLogAttached:
                                if bool(os.path.isdir(Config.TC_Temp_tcLog)):
                                        shutil.rmtree(Config.TC_Temp_tcLog)
                                        
                                os.mkdir(Config.TC_Temp_tcLog)
                                
                                Log.SaveToDisk()
                                                                
                                Directorys = os.listdir(Config.WAWi_AQC_Directory_Log)
                                DirectoryList = [Directory for Directory in Directorys]
                                DirectoryList.sort()
                                DirectoryList = DirectoryList[len(DirectoryList) - 2:]
                        
                                for it in DirectoryList:
                                        if os.path.isfile(Config.WAWi_AQC_Directory_Log + '\\' + it):
                                                shutil.copy(Config.WAWi_AQC_Directory_Log + '\\' + it, Config.TC_Temp_tcLog + '\\' + it)
                                                Delay(500)
                                        else:
                                                shutil.copytree(Config.WAWi_AQC_Directory_Log + '\\' + it, Config.TC_Temp_tcLog + '\\' + it)
                                                Delay(1000)
                                        
                                        
                                
                                ZipTCLog = Config.TestAppFolder + '\\tcLog.zip'
                                
                                if os.path.exists(ZipTCLog):
                                        os.remove(ZipTCLog)
                        
                                filePaths = []                                
                                
                                for root, directories, files in os.walk(Config.TC_Temp_tcLog):
                                        for filename in files:
                                                filePath = os.path.join(root, filename)
                                                filePaths.append(filePath)
                                
                                zipper = zipfile.ZipFile(Config.TC_Temp_tcLog + '.zip', 'w')
        
                                Delay(500)
                                
                                for file in filePaths:
                                        Directory = file[len(Config.TC_Temp_tcLog) + 1 :]
                                        zipper.write(file, Directory)
                                        Delay(1000)
                
                                zipper.close()                                
                                
                                if os.path.getsize(ZipTCLog)/1048576 < 13.5:
                                        attachment = open(ZipTCLog, "rb") 
                                        tempHolder = MIMEBase('application', 'zip') 
                                        tempHolder.set_payload((attachment).read()) 
                                        encoders.encode_base64(tempHolder) 
                                        tempHolder.add_header('Content-Disposition', 'attachment', filename = 'tcLog.zip')
                                        message.attach(tempHolder)
                                else:
                                        ListFileDirctoryOfSourceForUpload.append([Config.TestAppFolder, 'tcLog.zip'])
    
                                
                        if IseLogAttached:
                                if bool(os.path.isdir(Config.TC_Temp_eLog)):
                                        shutil.rmtree(Config.TC_Temp_eLog)                                
                        
                                Log.SaveResultsAs(Config.TC_Temp_eLog, 1, False)

                                Delay(500)
                                                        
                                ZipLog = Config.TestAppFolder + '\\eLog.zip'
                                                    
                                if os.path.exists(ZipLog):
                                        os.remove(ZipLog)
                        
                                filePaths = []
   
                                for root, directories, files in os.walk(Config.TC_Temp_eLog):
                                        for filename in files:
                                                filePath = os.path.join(root, filename)
                                                filePaths.append(filePath)

                                zipper = zipfile.ZipFile(Config.TC_Temp_eLog + '.zip', 'w')
                                Delay(500)
                                
                                for file in filePaths:
                                        Directory = file[len(Config.TC_Temp_eLog) + 1 :]
                                        zipper.write(file, Directory)
                                        Delay(50)
                
                                zipper.close()
                                
                                if os.path.getsize(ZipLog)/1048576 < 13.5:
                                        attachment = open(ZipLog, "rb") 
                                        tempHolder = MIMEBase('application', 'zip') 
                                        tempHolder.set_payload((attachment).read()) 
                                        encoders.encode_base64(tempHolder) 
                                        tempHolder.add_header('Content-Disposition', 'attachment', filename = 'eLog.zip')
                                        message.attach(tempHolder)
                                else:
                                        ListFileDirctoryOfSourceForUpload.append([Config.TestAppFolder, 'eLog.zip'])
                                        
                                        
                        if IseLogExportToftp:
                                ListFileDirctoryOfSourceForUpload.append([Config.TestAppFolder, 'eLog.zip'])
                                
                        self.__SendAttachmentToftp(Empfanger, ListFileDirctoryOfSourceForUpload)
                                
                        server = smtplib.SMTP(smtpserver)
                        server.starttls()
                        server.login(login,password)

                        server.sendmail(login, Empfanger, message.as_string())
                        server.quit()
        
                except Exception as exp:
                        Log.Warning("__EmailOperation: " + str(exp))
#--
#...
#--        
        def __SendAttachmentToftp(self, Empfanger, ListFileDirctoryOfSourceForUpload):
        
                try:
                        ListFileDirctoryOfSourceForUpload.pop(0)
        
                        if len(ListFileDirctoryOfSourceForUpload) == 0:
                                return
                                                       
                        DirectoryOfDistination = str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")) + '-' + Empfanger
                        DirectoryOfDistination = DirectoryOfDistination.replace('/', '-')
                        DirectoryOfDistination = DirectoryOfDistination.replace(',', '-')
                        DirectoryOfDistination = DirectoryOfDistination.replace('.', '-')
                        DirectoryOfDistination = DirectoryOfDistination.replace('@', '-')
                        DirectoryOfDistination = DirectoryOfDistination.replace(':', '-')
                        DirectoryOfDistination = DirectoryOfDistination.replace(' ', '-')
                        
                        self.ftpOperations(Methode = 'UploadWithCreateDirectory', ListFileDirctoryOfSourceForUpload = ListFileDirctoryOfSourceForUpload, DirectoryOfDistination = DirectoryOfDistination)
                
                except Exception as exp:
                        Log.Warning("__SendAttachmentToftp: " + str(exp))                    
#--
#...
#--
        def __CheckLokalAQC(self):
                
                try:
                
                        Temp = mDBOperation.cDBOperation()                        
                        DBmsg = Temp.DBC(Type = 'OnePropertyQRY', SQLCommand = "USE AQC;SELECT COUNT(1) FROM JOBS", SQLHost = Config.AQCHost)
                        
                        if DBmsg == 'DB Fehler':
                                Config.AQCHost = Config.SQLHost
                                DBmsg = Temp.DBC(Type = 'OnePropertyQRY', SQLCommand = "USE AQC;SELECT COUNT(1) FROM JOBS", SQLHost = Config.AQCHost)
                                
                                if DBmsg == 'DB Fehler':
                                        self.__SendRedirctAQCInfo()
                
                                        File = open(Config.WAWi_AQC_DB_Create_Script, "r")
                                        for line in File:
                                                line = line.replace('\n', '')
                                                line = line.replace('\t', '')
                                                line = line.replace('\'\'', '\'')
                                
                                                templine = line[0:4]
                                                if templine == 'AQC ':
                                                        DBNAME = 'AQC'
                                                else:
                                                        DBNAME = 'master'
                                                line = line[4:]
                                                Temp.DBC(Type = 'Command', SQLCommand = line, SQLHost = Config.AQCHost, Database = DBNAME)
                                        File.close() 
                        
                                        Config.AQCHost = Config.SQLHost
                        
                except Exception as exp:
                        Log.Warning("__CreateLokalAQC: " + str(exp))
#--
#...
#--
        def __SetTestPlattform(self):
                
                try:
                
                        OS_Proc_List = os.popen('tasklist').read().strip().split('\n')
        
                        for it in OS_Proc_List:
                                if it.find('TestComplete.exe') == 0:
                                        Config.TestPlatforms = 'TC'
                                        break
                                        
                                elif it.find('TestExecute.exe') == 0:
                                        Config.TestPlatforms = 'TE'
                                        break
                                        
                except Exception as exp:
                        Log.Warning("__SetTestPlattform: " + str(exp))
#--
#...
#--
        def __GetAktellDevVersion(self, IsChangeAktualVersion = True):
                
                try:
                
                        ReturnValue = self.__DownloadWAWiForSetup(IsGetListOfWAWiVersion = True)
                        
                        if IsChangeAktualVersion:
                                Config.AktualVersion = ReturnValue[ReturnValue.find('_') + 1:ReturnValue.find('.exe')]
                                Config.SetupVersion = ReturnValue
                                
                        return ReturnValue
                                        
                except Exception as exp:
                        Log.Warning("__GetAktellDevVersion: " + str(exp))
#--
#...
#--
        def __ExternalLockAndCommandTurn(self):
                
                try:
                
                        ExternalModeStatus = None
                        
                        Temp = mDBOperation.cDBOperation()
                        ExternalModeStatus = Temp.DBC(Type = 'OnePropertyQRY', SQLCommand = "USE AQC;SELECT [Value] FROM Config WHERE Config = \'IsInExternalMode\'", SQLHost = Config.AQCHost).strip()
                        
                        if ExternalModeStatus != 'False':
                                while Temp.DBC(Type = 'OnePropertyQRY', SQLCommand = "USE AQC;SELECT [Value] FROM Config WHERE Config = \'IsInExternalMode\'", SQLHost = Config.AQCHost).strip() != 'False':
                                        Delay(100000)

                        self.__TurnLockOperation()
                        
                except Exception as exp:
                        Log.Warning("__ExternalLockAndCommandTurn " + str(exp))
#--
#...
#--
        def __TurnLockOperation(self, Operat = 'CheckLock'):
                
                try:
                
                        Temp = mDBOperation.cDBOperation()
                        
                        if Operat == 'CheckLock':
                                Lockturn = Temp.DBC(Type = 'OnePropertyQRY', SQLCommand = "USE AQC;SELECT [Value] FROM Config WHERE Config = \'Lockturn\'", SQLHost = Config.AQCHost).strip()
                        
                                if Lockturn != 'False':
                                        while Temp.DBC(Type = 'OnePropertyQRY', SQLCommand = "USE AQC;SELECT [Value] FROM Config WHERE Config = \'Lockturn\'", SQLHost = Config.AQCHost).strip() != 'False':
                                                Delay(6000)
                                                                      
                        elif Operat == 'Lock':
                                Temp.DBC(Type = 'Command', SQLCommand = "USE AQC;UPDATE Config SET [Value] = \'True\' WHERE Config = \'Lockturn\'", SQLHost = Config.AQCHost)
                                
                        elif Operat == 'ReleseLock':
                                Temp.DBC(Type = 'Command', SQLCommand = "USE AQC;UPDATE Config SET [Value] = \'False\' WHERE Config = \'Lockturn\'", SQLHost = Config.AQCHost)
                                        
                except Exception as exp:
                        Log.Warning("__TurnLockOperation: " + str(exp))
#--
#...
#--
        def __ChangeCommandTurn(self, Operat = 'Increase'):
                
                try:
                
                        Temp = mDBOperation.cDBOperation()
                        
                        FetchPriority = Temp.DBC(Type = 'OnePropertyQRY', SQLCommand = "USE AQC;SELECT [Value] FROM Config WHERE Config = \'FetchPriority\'", SQLHost = Config.AQCHost).strip()
                                
                        if Operat == 'Increase':
                                FetchPriority = '\'' + str(int(FetchPriority[1: len(FetchPriority) - 1]) + 1) + '\''
                                
                        elif Operat == 'Decrease':
                                if int(FetchPriority[1: len(FetchPriority) - 1]) <= 1:
                                        FetchPriority = '1'
                                        
                                FetchPriority = '\'' + str(int(FetchPriority[1: len(FetchPriority) - 1]) - 1) + '\''
                                
                        #inja agar external bod bayad yeki ziyad beshe ta 2 ta external posht sar ham ejra nashan
                        self.CommandTurn = '1'

                                        
                except Exception as exp:
                        Log.Warning("__TurnLockOperation: " + str(exp))
#--
#...
#--
        def __ClearBackups(self):
            
                try:
                
                        Temp = mDBOperation.cDBOperation()
                        
                        BackupPath = Temp.DBC(Type = 'OnePropertyQRY', SQLCommand = "USE master; DECLARE @BackupDirectory NVARCHAR(100); EXEC master..xp_instance_regread @rootkey = \'HKEY_LOCAL_MACHINE\', @key = \'Software\\Microsoft\\MSSQLServer\\MSSQLServer\', @value_name = \'BackupDirectory\', @BackupDirectory = @BackupDirectory OUTPUT; SELECT @BackupDirectory AS [DefaultBackupPath]", SQLHost = Config.SQLHost).strip()
                        
                        for BackupFile in os.listdir(BackupPath):
                                os.remove(BackupPath + '\\' +BackupFile)
                                        
                except Exception as exp:
                        Log.Warning("__ClearBackups: " + str(exp))
#--
#...
#--
        def __ClearOneDrive(self):
            
                try:

                        for TempFile in os.listdir(Config.TC_Sample_Datei_Directory):
                                if TempFile.find('QAS') >= 0:
                                        os.remove(Config.TC_Sample_Datei_Directory + '\\' + TempFile)                                
                                        
                except Exception as exp:
                        Log.Warning("__ClearOneDrive: " + str(exp))