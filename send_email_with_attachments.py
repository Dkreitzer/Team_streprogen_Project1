##https://github.com/TeCoEd/Whats-News/tree/master/Code
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
# in the config.py file, we put the senders's gmail accountand&password in the following form:
#EMAIL_ADDRESS=" " 
#PASSWORD=" "  
#from config  import EMAIL_ADDRESS,PASSWORD
import os 
EMAIL_ADDRESS= os.environ.get("EMAIL_ADDRESS")
PASSWORD= os.environ.get("PASSWORD")
# subject = "sending email with attachments"
# body = 'Hi there, we are sending this email from Python!'
### Function to send the email ###
def send_an_email(file_name,subject="sending email with attachments",\
            body='from Python!'):
    #global subject,body
    ##add xander and jeff's emails here:

    #toaddr_s = ['yjjiangphysics@gmail.com','Kreitzer.gr@gmail.com','xanendorf@gmail.com']
    toaddr_s = ['yjjiangphysics@gmail.com']
    #,'Kreitzer.gr@gmail.com'] 
    me =  EMAIL_ADDRESS
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = 'yjjiangphysics@gmail.com'
    msg.preamble = "test " 
    msg.attach(MIMEText(body,'plain'))

    part = MIMEBase('application', "octet-stream")

    #put the attachments in the following, once in the open(?),
    #once in the filename=?. The second ? is only to ensure the 
    #right file format:
    part.set_payload(open(file_name, "rb").read())
    encoders.encode_base64(part)
    part.add_header(f'Content-Disposition', f'attachment; filename={file_name}')
    msg.attach(part)

    try:
       s = smtplib.SMTP('smtp.gmail.com', 587)
       s.ehlo()
       s.starttls()
       s.ehlo()
       s.login(EMAIL_ADDRESS, PASSWORD)
       #s.send_message(msg)
       aa=[s.sendmail(me, toaddr, msg.as_string()) for toaddr in toaddr_s]
       s.quit()
    
    #except:
    #   print ("Error: unable to send email")
#https://stackoverflow.com/questions/13957829/how-to-use-raise-keyword-in-python
#https://www.youtube.com/watch?v=b0PAVVchc7c
    except Exception as e:
          print (e)
    finally:
        pass
          

# file="..//try.html"
# send_an_email(file)