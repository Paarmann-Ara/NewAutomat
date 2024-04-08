from services.mail.core.base_mail import BaseMail
from services.mail.config.mail_config import MailConfig
from services.mail.templates.mail_template_dictionary import MailTemplateDictionary
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib
import os
from typing import Any

# --
# ...
# --


class Mail(BaseMail):
    def __init__(self, **kwargs) -> None:      
        
        try:
            
            self.to_addr_list = []
            self.cc_addr_list = []

            #set template
            if 'template' in kwargs:
                self.mail_template_class = self.instance.template_dictionary[kwargs['template']]
                self.template_object = self.mail_template_class(body='').template_object

                if 'template_body' in kwargs:
                    self.template_object = self.mail_template_class(body=kwargs['body']).template_object
                    
            self.subject = kwargs['subject']

            #set domain
            if 'domain' in kwargs:
                self.domain_dictionary = self.instance.config_dictionary[kwargs['domain']]
                self.smtpserver=self.domain_dictionary['smtp']
                
                #create and set from adresss dictionary
                self.from_addr=self.domain_dictionary[kwargs['sender']]['address']
                self.password=self.domain_dictionary[kwargs['sender']]['password']
                
                #create and set to, cc adresss dictionary
                recipient_dictionary = kwargs['recipient']
                 
                for item in recipient_dictionary['recipient_address']:
                    self.to_addr_list.append(self.domain_dictionary[item])
                
                for item in recipient_dictionary['recipient_cc']:
                    self.cc_addr_list.append(self.domain_dictionary[item])

            #attchment
            #   attach_object = {'attach_item' : {'is_attach' : True, 'is_all_directory' : False, 'directory' : '', 'file' :''}}
            if 'attach_object' in kwargs:
                self.attach_object = kwargs['attach_object']
                 
        except Exception as exp:
           self.error(f"{__file__}--->{__name__}: {str(exp)}")
            
#--
#...
#--

    @classmethod
    def get_template_dictionary(cls):
            return MailTemplateDictionary()()
        
#--
#...
#--

    @classmethod
    def get_config_dictionary(cls):
            return MailConfig().instance.dictionary
       
# --
# ...
# --
    
    def send_mail(self, **kwargs) -> bool:
        
        try:

            # high periority is for parameter that sent to send_mail then attributs of mail instance
            if 'template_object' in kwargs:
                template_object = kwargs['template_object']
            else:
                template_object = self.template_object
                
            if 'subject' in kwargs:
                subject = kwargs['subject']
            else:
                subject = self.subject
                
            if 'attach_object' in kwargs:
                attach_object = kwargs['attach_object']
            else:
                attach_object = self.attach_object
                
            message = MIMEMultipart('alternative')
            message['From'] = self.from_addr
            message['subject'] = subject
            message['Cc'] = ','.join(self.cc_addr_list)

            body = MIMEText(template_object['body'], 'plain')
            html = MIMEText(template_object['mixed_html'], 'html')

            message.attach(body)
            message.attach(html)
            
            if attach_object is not None:
                for attached_file in self.attachment_manager(attach_object):
                    message.attach(attached_file)

            server = smtplib.SMTP(self.smtpserver)
            server.starttls()
            server.login(self.from_addr, self.password)

            for to_addr in self.to_addr_list:
                message['To'] = to_addr
                server.sendmail(self.from_addr, to_addr, message.as_string())
                
            server.quit()
            
            return True

        except Exception as exp:
            self.error(f"{__file__}--->{__name__}: {str(exp)}")
            return False

# --
# ...
# --

    def attachment_manager(self, attach_object=None) -> Any:
        
        if attach_object is None : return
        
        try:
            
            files = []
            attachments = []
            
            for item in attach_object:
                item = attach_object[item]
                is_attach = item['is_attach']
                is_all_directory = item['is_all_directory']
                directory = item['directory']
            
                if is_attach:
                    if bool(os.listdir(directory)):
                        
                        if is_all_directory:
                            for Item in os.listdir(directory): files.append(directory + '#' + item['file'])
                        else:
                            files.append(directory + '#' + item['file'])
                            
            attachments = self.create_holder(files)

            return attachments
                    
        except Exception as exp:
            self.error(f"{__file__}--->{__name__}: {str(exp)}")
            
# --
# ...
# --

    def create_holder(self, files):
        
        try:
            
            temp_attachments = []
            files = set(files)
            #f = list(dict.fromkeys(File))
            _ = 0
                
            for item in files:
                item = item.split('#')
                item = '/'.join(item)
                attachment = open(item, "rb")
                
                temp_attachments.append(MIMEBase('application', 'octet-stream'))
                temp_attachments[_].set_payload((attachment).read())
                encoders.encode_base64(temp_attachments[_])
                
                temp_attachments[_].add_header(
                    'Content-Disposition', "attachment; filename= %s" % item[1])
                
                _ += 1
                
            return temp_attachments
        
        except Exception as exp:
            self.error(f"{__file__}--->{__name__}: {str(exp)}")

