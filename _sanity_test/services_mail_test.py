from services.mail.templates.testcomplete_result import TestCompleteResultTemplate
from services.mail.mail_provider import MailProvider
from jtl_wawi.testcase.testcase_sample_provider import TestcaseSampelProvider

tc_mo = MailProvider().tc_mo_instance
tc_mo.send_mail()

tc_mo = MailProvider(body='Test_body', subject='Test_Subjekt').tc_mo_instance
tc_mo.send_mail()

template_object = TestCompleteResultTemplate(body='BODY Ke Sakhtam').template_object
tc_mo.send_mail(template_object=template_object)

Simple_CSV_AnhangDatei = TestcaseSampelProvider('Simple_CSV_AnhangDatei')
xmlAuftrageDatei = TestcaseSampelProvider('xmlAuftrageDatei')

attach_object = {
    'AttachItem_0' : {
            'is_attach' : True, 
            'is_all_directory' : False,
            'directory' : Simple_CSV_AnhangDatei.directory, 
            'file' : Simple_CSV_AnhangDatei.file
        },

    'AttachItem_1' : {
            'is_attach' : True, 
            'is_all_directory' : False,
            'directory' : xmlAuftrageDatei.directory, 
            'file' : xmlAuftrageDatei.file
        },
    }

tc_mo.send_mail(attach_object=attach_object)
