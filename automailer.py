import smtplib
from configparser import ConfigParser 

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import os
from email import encoders
import logging 
configur = ConfigParser() 
logging.basicConfig(filename="monitoring.log", 
                    format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    filemode='a',
                    datefmt = '%d/%m/%Y %I:%M:%S %p' )
logger=logging.getLogger() 
  
logger.setLevel(logging.DEBUG) 
configur.read('config.ini')
logger.info('Just Read config file Mail Items.')
userName= configur.get('mail','userName')
password= configur.get('mail','password')
cc= configur.get('mail','cc')
to= configur.get('mail','to')
print(userName,password)
print(cc)
print(to)

msg = MIMEMultipart('alternative')
msg['Subject'] = "TradeTech "
msg['From'] = userName
msg['To'] = (to)
msg['Cc']=(cc)
message="Testing mail ..........."
html = """\
<html>
  <head></head>
  <body>
    <p>Dear Team ,<br>
    <br>
       		Find the attachement for your information on list of Stock's <br>
     <br>
     Thanks & Regards,<br>
     Vennam BOT
    </p>
  </body>
</html>
"""


part2 = MIMEText(html, 'html')
part1 = MIMEText(message, 'plain')
msg.attach(part1)
msg.attach(part2)
# open the file to be sent  
filename = "Market_Stock_Id_List.csv"
attachment = open(filename, "rb") 
  
# instance of MIMEBase and named as p 
p = MIMEBase('application', 'octet-stream') 
  
# To change the payload into encoded form 
p.set_payload((attachment).read()) 
  
# encode into base64 
encoders.encode_base64(p) 
   
p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
# attach the instance 'p' to instance 'msg' 
msg.attach(p) 

recpt=cc.split(',')+to.split(',')

try:
   logger.info('Started the mail process.')
   smtp = smtplib.SMTP('smtp.gmail.com',587)
   smtp.ehlo()
   smtp.starttls()
   smtp.login(userName,password)

   smtp.sendmail(userName, recpt, msg.as_string())  
   smtp.quit()       
   print ("Successfully sent email")
   logger.info(f'Mail has been sent to {recpt}.')
except Exception as e:
   logger.Error(f'Exception at mail sending process: {e}')
   print ("Error: unable to send email")
   print(e)
