# Send Message

import smtplib

# FRIENDLY NAME
# isTaker

# SID
# SKbc809064ab275d4402380c5b5dbbdc87

# KEY TYPE
# Standard

# SECRET
# VCl1P6KAQzeOnnEjodG5h2OcCSkrGb14

def send_message_to_available_service_boy(service_boys, Your_Order):
    # print(Your_Order)

    # for service_boy in service_boys:
    mail_server = smtplib.SMTP('smtp.gmail.com', 587)
    mail_server.starttls()
    mail_server.login("vermakaustubh28@gmail.com", "uvbulppoaoxlwzhu")
    SUBJECT = "New Request"   
    TEXT = str(Your_Order)

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    mail_server.sendmail('&&&&&&&&&&&', service_boys[0].email, message)
    # print(service_boys[0].email)
