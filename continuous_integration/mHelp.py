import time
import os
from importlib.machinery import SourceFileLoader
import imaplib
import codecs
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import datetime
import smtplib
import sys
import getopt

#--
#...
#--
class Help():
        def __init__(self):
                self.Delay                                                                                                                      = 1200
                self.Absender                                                                                                                   = ''
                self.HelpText                                                                                                                   = ''
                self.ListTestMe                                                                                                                 = []
                
                self.TC_Help_Address                                                                                                            = 'tc-help@jtl-software.de'#'TC-Help@outlook.de'
                self.TC_Help_Password                                                                                                           = '6Cwee$64xapH6!50'#'@25340Pedram'
                self.TC_MailServer                                                                                                              = 'mail.jtl-software.de'#'smtp.office365.com'
                self.TC_MailServer_SMTP                                                                                                         = 'mail.jtl-software.de:587'#'smtp.office365.com:587'
                self.WAWi_AQC_Directory_Script                                                                                                  = r'C:\OneDrive\TC\AQC\WAWi\Script'
                self.Help_Prototype_Module_Address                                                                                              = r'C:\OneDrive\TC\AQC\WAWi\Script'
                self.Help_TEXT_Address                                                                                                          = r'C:\OneDrive\Manager\Help.txt'
                self.Help_Temp_Module_Address                                                                                                   = r'C:\OneDrive\Manager\HelpTemp.py'
                self.Help_Template_Address                                                                                                      = r'C:\OneDrive\Manager\HelpTemplate.txt'
                
                self._Repository_Help_Address 						                                                                            = r'C:\OneDrive\TC_Sample_Datei\_TestHelpMe.txt'
                self.NoReplay_Address                                                                                                           = r'tc@jtl-software.de'
                self.NoReplay_Password                                                                                                          = r'Gk%30lh7uZy!h919'
                self.NoReply_MailServer_SMTP                                                                                                    = r'mail.jtl-software.de:25'
                
        
#--
#...
#--        
        def Start(self):
    
                try:

                        LoginConf = ''
                        LoginData = None
                        TYP = ''
                        email_user = self.TC_Help_Address
                        email_pass = self.TC_Help_Password
                        
                        Counter = 0
                        
                        sys.path.append(self.WAWi_AQC_Directory_Script)
                        
                        while True :                   

                                try:
                                
                                        self.__loging(str(Counter))
                                    
                                        M = imaplib.IMAP4(self.TC_MailServer)
                                        LoginConf, LoginData = M.login(email_user, email_pass)
                        
                                        while LoginConf != 'OK':
                                                time.sleep(60)
                                                LoginConf, LoginData = M.login(email_user, email_pass)                        
                                
                                        TYP, MsgData = M.select('INBOX')
                        
                                        while TYP != 'OK':
                                                time.sleep(60)
                                                TYP, MsgData = M.select('INBOX')
                                        
                                        CountMsg = int(MsgData[0])
                        
                                        M.close()
                                        M.logout() 
                                
                                        if CountMsg > 0:
                                                if self.Absender != 'MAILER-DAEMON@mail.jtl-software.de':
                                                        self.__FetchCommand()
                                                        self.__RefreshCommand()
                                                        self.__SendHelpMail(self.Absender)
                                                        time.sleep(6)
                                                                
                                                self.__RefreshCommand()
                                
                                        self.__RefreshOneDrive()
                                        
                                        time.sleep(self.Delay)
                                
                                except Exception as exp:
                                        Log.Warning("HelpStart: " + str(exp))
                                    
                                finally:
                                        Counter += 1
            
                except Exception as exp:
                        self.__loging('Start: ' + str(exp))
#--
#...
#--
        def __FetchCommand(self):
    
                try:
    
                        email_user = self.TC_Help_Address
                        email_pass = self.TC_Help_Password
                        M = imaplib.IMAP4(self.TC_MailServer)
                        M.login(email_user, email_pass)

                        M.select('INBOX', readonly=True)

                
                        typ, msg_data = M.fetch('1', '(BODY.PEEK[HEADER])')
                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                Header = response_part[1].decode("utf-8")
                                result = Header.find('<') + 1
                                Header = Header[result:]
                                result = Header.find('>')
                                self.Absender = Header[0:result]
                                self.__loging(self.Absender)
                
                
                        typ, msg_data = M.fetch('1', '(BODY.PEEK[TEXT])')
                        
                        for response_part in msg_data:
                                if isinstance(response_part, tuple): 
                                        msg = response_part[1].decode("utf-8")
                                        msg = self.__DecodeMessage(msg)
                                        
                        M.close()
                        M.logout()
            
                except Exception as exp:
                    self.__loging('__FetchCommand: ' + str(exp))
#--
#...
#--
        def __DecodeMessage(self, Msg):
                
                try:
        
                        CommandString = ''
                        
                        result = Msg.find('#') + 1
                        Msg = Msg[result:]
                        result = Msg.find('#')
                        Msg = Msg[0:result]
                                
                        Msg = Msg.replace("=3D", "=")

                        Msg = Msg.split('\n')
                        
                        for Command in Msg:
                                self.__loging(Command)
                                
                                if (Command == '\r' or Command == '\n' or Command == '\t'):
                                    continue
                                    
                                Command = Command.strip()
                        
                                if Command[0:1] == '$':
                                        CommandString = Command[1:]
                                        self.CreateHelpText('m' + CommandString)
                                        self.__loging(CommandString)
                                        break

                                elif Command[0:1] == '?':
                                        self.GetAllModuls()
                                        break
                                        
                                else:
                                        self.GetAllModuls() 
                                        break                                       
                        
                except Exception as exp:
                        self.__loging('__DecodeMessage: ' + str(exp))
#--
#...
#--          
        def __RefreshCommand(self):
    
                try:
    
                        email_user = self.TC_Help_Address
                        email_pass = self.TC_Help_Password
                        M = imaplib.IMAP4(self.TC_MailServer)
                        M.login(email_user, email_pass)

                        M.select('INBOX')

                        M.store('1', '+FLAGS', r'(\Deleted)')
                
                        M.expunge()
                        
                        M.close()
                        M.logout()    
            
                except Exception as exp:
                        self.__loging('__RefreshCommand: ' + str(exp))
#--
#...
#--          
        def __RefreshOneDrive(self):
    
                try:
    
                        if os.path.exists(self.Help_TEXT_Address):
                                os.remove(self.Help_TEXT_Address)
                                
                        if os.path.exists(self.Help_Temp_Module_Address):
                                os.remove(self.Help_Temp_Module_Address)
                                                               
                except Exception as exp:
                        self.__loging('__RefreshOneDrive: ' + str(exp))
#--
#...
#--        
        def GetAllModuls(self):
    
                try:

                        tempHelpSrting = 'Moduls: \n\n'
                        tempTemplate = ''
                        
                        NoShowModuls = ['AdressAusWahlen', 'ArtikelAuswahlen_winform', 'ArtikelAuswahlen_wpf', 'Base', 'CheckPoint', 'CheckPoint', 'CheckPointSelector', 'CU', 'DBOperation', 'Exception', 'File', 'Html', 'jtlInputbox', 'ListView', 'ListViewEditor', 'ListViewToolbar', 'Objects', 'Server', 'TextAndTime', 'Toolbar', 'Toolsbar']

                        AlleModuls = [AllModul[1:len(AllModul) - 3] for AllModul in os.listdir(self.WAWi_AQC_Directory_Script) if AllModul.startswith('m') and not AllModul.endswith('.bak')]
                        Moduls = [Modul for Modul in AlleModuls if Modul not in NoShowModuls]

                        for Modul in Moduls:
                                tempHelpSrting = tempHelpSrting + 2*'\t' + Modul + '\n'
                                
                        if os.path.exists(self.Help_Template_Address):
                                with open(self.Help_Template_Address , 'r') as code:
                                        tempTemplate = code.read()

                        tempHelpSrting = tempTemplate + tempHelpSrting

                        with open(self.Help_TEXT_Address , 'w') as code:
                                code.write(tempHelpSrting)
                                
                except Exception as exp:
                        self.__loging('GetAllModuls: ' + str(exp))
#--
#...
#--        
        def CreateHelpText(self, Modul):
    
                try:
                
                        Modul = self.__PrototypeMaker(Modul)
                        
                        if os.path.exists(self.Help_TEXT_Address):
                                os.remove(self.Help_TEXT_Address)

                        tempHelpSrting = '\ndef Start():\n'
        
                        tempHelpSrting = tempHelpSrting + 2*'\t' + 'import ' + Modul + '\n'
                        tempHelpSrting = tempHelpSrting + 2*'\t' + 'Object = ' + Modul + '.c' + Modul[2:] + '()\n'

                        tempHelpSrting = tempHelpSrting + 2*'\t' + 'NoShowAttribute = [\'Mode\', \'QProjection\', \'QSource\', \'QCondition\' , \'Empfanger\', \'War\', \'Ist\', \'CheckList_0_Ar\', \'CheckList_0_Ar_Antwort\', \'CheckList_0_DIC_Antwort\', \'CheckList_0_DB_Att\', \'CheckList_0_Ar_Ext\', \'CheckList_0_DB_Att_Ext\', \'CheckPoint_Dic\']\n'
                        tempHelpSrting = tempHelpSrting + 2*'\t' + 'attribute_list = [key + \' = \' + str(value) for key, value in Object.__dict__.items() if not key in NoShowAttribute]\n'
                        tempHelpSrting = tempHelpSrting + 2*'\t' + 'method_list = [method for method in dir(Object) if method.startswith(\'MainMenu\') or method.startswith(\'ToolbarPage\')]\n\n\n'

                        tempHelpSrting = tempHelpSrting + 2*'\t' + 'tempModule = \'Module: ' + Modul[1:] + '\'\n'
                        tempHelpSrting = tempHelpSrting + 2*'\t' + 'tempAttribute = \'Attributes: \'+ \'\\n\' \n\n'
                        tempHelpSrting = tempHelpSrting + 2*'\t' + 'tempMethod = \'Methods: \'+ \'\\n\' \n\n'
                        tempHelpSrting = tempHelpSrting + 2*'\t' + 'for attribute in attribute_list:\n'
                        tempHelpSrting = tempHelpSrting + 4*'\t' + 'tempAttribute = tempAttribute + 2*\'\t\' + attribute + \'\\n\' \n\n'
                        tempHelpSrting = tempHelpSrting + 2*'\t' + 'for method in method_list:\n'
                        
                        
                        
                        tempHelpSrting = tempHelpSrting + 4*'\t' + 'methodStringList = method.split(\'_\')\n'
                        tempHelpSrting = tempHelpSrting + 4*'\t' + 'rest = \'\' \n'
                        tempHelpSrting = tempHelpSrting + 4*'\t' + 'Startposition =  5 * \'\t\' + \'-->Startposition: auf \' + methodStringList[0]' + '\n'
                        tempHelpSrting = tempHelpSrting + 4*'\t' + 'Bereich =  \'\\n\'+ 5 * \'\t\' + \'-->im: \' + methodStringList[2]' + '\n'
                        tempHelpSrting = tempHelpSrting + 4*'\t' + 'Durch =  \'\\n\'+ 5 * \'\t\' + \'-->durch: \' + methodStringList[3]'  + '\n'
                        tempHelpSrting = tempHelpSrting + 4*'\t' + 'methodStringList = methodStringList [4 :]' + '\n'
                        tempHelpSrting = tempHelpSrting + 4*'\t' + 'methodStringListLen = methodStringList' + '\n'
                        tempHelpSrting = tempHelpSrting + 4*'\t' + 'for word in methodStringListLen:' + '\n'
                        tempHelpSrting = tempHelpSrting + 6*'\t' + 'rest = rest + word + \' \' \n'
                        tempHelpSrting = tempHelpSrting + 4*'\t' + 'Beschreibung =  \'\\n\'+ 5 * \'\t\' + \'-->Aktion: \' + rest ' + '\n' 
                        tempHelpSrting = tempHelpSrting + 4*'\t' + 'MethodBeschreibung = \'\' + Startposition + Bereich + Durch + Beschreibung \n'

                        
                        
                        tempHelpSrting = tempHelpSrting + 4*'\t' + 'tempMethod = tempMethod + 2*\'\t\' + method + \'\\n\' + MethodBeschreibung + 2 * \'\\n\' \n\n'
                        
                        tempHelpSrting = tempHelpSrting + 2*'\t' + 'Help_TEXT = tempModule + \'\\n\'+ tempMethod + \'\\n\'+ tempAttribute\n\n'
                        tempHelpSrting = tempHelpSrting + 2*'\t' + 'with open(r\'' + self.Help_TEXT_Address + '\' , \'w\') as code:\n'
                        tempHelpSrting = tempHelpSrting + 4*'\t' + 'code.write(Help_TEXT)'
                        tempHelpSrting = tempHelpSrting + '\n\n'
                        
                                                                                       
                        with open(self.Help_Temp_Module_Address , 'w') as code:
                                code.write(tempHelpSrting)

                        Cmd = None

                        MName,FileExt = os.path.splitext(os.path.split(self.Help_Temp_Module_Address)[-1])

                        if FileExt.lower() == '.py':
                            #mPy = imp.load_source(MName, self.Help_Temp_Module_Address)
                            mPy = SourceFileLoader(MName, self.Help_Temp_Module_Address).load_module()

                        if hasattr(mPy, 'Start'):
                            Cmd = getattr(mPy, 'Start')()
                            
                        if os.path.exists(self.Help_Prototype_Module_Address):
                                os.remove(self.Help_Prototype_Module_Address)

                except Exception as exp:
                        self.__loging('CreateHelpText: ' + str(exp))
#--
#...
#--                        
        def __PrototypeMaker(self, moduleName):
                
                try:
                
                        self.Help_Prototype_Module_Address = r'C:\OneDrive\TC\AQC\WAWi\Script'
                        modulePath = self.WAWi_AQC_Directory_Script + '\\' + moduleName + '.py'
                        
                        if os.path.exists(modulePath):
                                with open(modulePath , 'r') as code:
                                        prototypeModule = code.read()
                                        
                                prototypeModulearray = prototypeModule.split('\n')
                                
                                prototypeModule = ''
                                flag = False
                                
                                for line in prototypeModulearray:
                                        if (line.find('import') > -1 or line.find('super(') > -1 or line.find('#') > -1):
                                                continue
                                        
                                        elif (line.find('Objects_') > -1 ):
                                                startPosition = line.find('Objects_')
                                                endPosition = line.find('.', startPosition - 1)
                                                objectWord = line[startPosition:endPosition + 1]
                                                line = line.replace(objectWord, '')
                                                
                                        elif (line.startswith('class')):
                                                line = 'class c' + moduleName[1:] + '():'
                                                
                                        elif (line.find('mRandom') > -1):
                                                startPosition = line.find('mRandom')
                                                line = line[:startPosition] + ' \'\' '
                                                
                                        #elif (line.find('self.CheckPoint_Dic') > -1):
                                         #       line = line.replace('Config.', '')
                                                
                                        elif (line.find('mTextAndTime') > -1): 
                                                startPosition = line.find('mTextAndTime')
                                                line = line[:startPosition] + '\'\''
                                                
                                        if (line.find('self.CheckPoint_Dic = {') > -1): 
                                                flag = not flag
                                                continue
                                                
                                        if flag:
                                                if (line.find('}') > -1):
                                                        flag = not flag
                                                continue
                                        
                                        prototypeModule = prototypeModule + '\n' + line
                                 
                                        
                                prototypeModule = 'from AQC.Setting.TestApp import Config\n' + prototypeModule
                                
                                self.Help_Prototype_Module_Address = self.Help_Prototype_Module_Address + '\\a' + moduleName + '.py'
                                
                                with open(self.Help_Prototype_Module_Address , 'w') as code:
                                        code.write(prototypeModule)
                                        
                                return 'a' + moduleName

                except Exception as exp:
                        self.__loging('__PrototypeMaker: ' + str(exp))

#--
#...
#--
        def __SendHelpMail(self, Empfanger):
                
                try:
                
                        subject = 'TestComplete, Hilfe'
                        HTML = """\<html></html>"""
                        HelpText = ""
                        
                        if os.path.exists(self.Help_TEXT_Address):
                                with open(self.Help_TEXT_Address , 'r') as code:
                                        HelpText = code.read()
                        
                        Node = os.environ['COMPUTERNAME']
                        User = os.getlogin()
                        
                        Body = '<h1>Hallo,</h1>\nDas Host: ' + Node + '\nDer Benutzer: ' + User + '\n</h3>wie gewunscht Hilfe wird der von Dir am ' + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ' gesendet.\n\n' + HelpText + '</h3>\n\n<h2>Ihr TC-Team</h2>'
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
                        self.__loging('__SendHelpMail: ' + str(exp))
#--
#...
#--
        def __EmailOperation(self, Empfanger, subject, Body, HTML):
                
                try:
                
                        login = self.TC_Help_Address
                        password = self.TC_Help_Password
                        smtpserver= self.TC_MailServer_SMTP
                                                               
                        message = MIMEMultipart('alternative')
                        message['subject'] = subject
                        message['From'] = login

                        Body =  MIMEText(Body, 'plain')
                        HTML = MIMEText(HTML, 'html')
                        
                        message.attach(Body)
                        message.attach(HTML)
                        
                        if os.path.exists(self.Help_TEXT_Address):                        
                                filename = "Help.Txt"
                                attachment = open(self.Help_TEXT_Address, "r") 
                                tempHolder = MIMEBase('application', 'octet-stream') 
                                tempHolder.set_payload((attachment).read()) 
                                encoders.encode_base64(tempHolder) 
                                tempHolder.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
                                message.attach(tempHolder)

                        server = smtplib.SMTP(smtpserver)
                        server.starttls()
                        server.login(login,password)

                        server.sendmail(login, Empfanger, message.as_string())
                        server.quit()
                        
                        self.__loging(20 * '.' + ' Mail Sent an: ' + Empfanger + ' ' + 20 * '.')
        
                except Exception as exp:
                        self.__loging('__EmailOperation: ' + str(exp))
#--
#...
#--

        def TestMe(self):
    
                try:

                        self.FillListTestMe()
                               
                        while len(self.ListTestMe) > 0:
                                mail = self.ListTestMe.pop(0)
                                self.TestMe_SendMail(mail)
                                       
                                        
                except Exception as exp:
                        self.__loging('TestMe: ' + str(exp))
#--
#...
#--
        
        def FillListTestMe(self):
    
                try:

                        if len(self.ListTestMe) == 0:
                                Text = ''
                                Keeper = 0
                
                                File = open(self._Repository_Help_Address, "r")
                
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
                        self.__loging('FillListTestMe: ' + str(exp))
#--
#...
#--

        def TestMe_SendMail(self, Body = ''):
    
                try:
    
                        Subject = 'TestTCServer'
                        Sender = self.NoReplay_Address
                        Password = self.NoReplay_Password
                        SmtpServer= self.NoReply_MailServer_SMTP
                
                        To = self.TC_Help_Address
                
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
                        
                        time.sleep(5)
            
                except Exception as exp:
                        self.__loging('TestMe_SendMail: ' + str(exp))
#--
#...
#--
        def __loging(self, log):

                try:    
                
                        print(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ':' + 5*'  ' + log)
        
                except Exception as exp:
                        print('__loging: ' + str(exp))
#--
#...
#--
def main(getArguments):

        try:    
                Delay = 600
                IsTest = False
        
                Params, Arguments = getopt.getopt(getArguments, "d:")
        
                for param, value in Params:
                        if param in ['-d']:
                                Delay = int(value)
                        elif param in ['-t']:
                                IsTest = True
    
        
                obj = Help()
                obj.Delay = Delay
                if (IsTest):
                        obj.TestMe()
                else:
                        obj.Start()   
                        
                sys.exit()
        
        except Exception as exp:
                print('main: ' + str(exp))
#--
#...
#--
if __name__ == "__main__":
        main(sys.argv[1:])                    