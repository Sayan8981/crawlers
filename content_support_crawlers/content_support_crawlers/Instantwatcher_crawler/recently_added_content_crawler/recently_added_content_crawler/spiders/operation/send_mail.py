import smtplib,ssl
import sys
import os
import socket
import csv
import ntpath
from datetime import datetime,timedelta
from email.mime.base import MIMEBase 
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class send_emails:

    def __init__(self):
        self.sender_email=''
        self.receiver_email=''
        self.password=''

    def user_input(self):
        self.sender_email="saayan@headrun.com"
        self.receiver_email=["hott@headrun.com"]
        self.password="9891274567"

    def user_message(self):
        text="""Hi Team,


    Instantwatcher recently added content Amazon service with Subscription [New Prime, New Rental, Purchase].
        
    Please find the attachment.

    


    With best regards,
    Saayan Das, """
    
        return text  

    def read_attachment(self,attachment_):
        with open(attachment_, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)
            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                "attachment", filename=ntpath.basename(attachment_)) 
            return part     

    def main(self):
        self.user_input()
        message=MIMEMultipart("alternative")
        message["Subject"]="Instantwatcher Amazon Result on %s"%(datetime.now() - timedelta(days=1)).strftime('%b %d, %Y')
        message["From"]=self.sender_email
        message["To"]=",".join([email_id for email_id in self.receiver_email])
        port =587
        text=self.user_message()
        part1=MIMEText(text,"plain")
        message.attach(part1)
        filenames=['recently_added_content_amazon_%s.csv'%(datetime.now().strftime('%b %d, %Y'))]
        for file in filenames:
            with open(os.getcwd()+'/operation/attachments/'+file, 'r') as csvfile:
                csv_dict = [row for row in csv.DictReader(csvfile)]
                print("data_committed count:", len(csv_dict))
                if len(csv_dict) > 1:
                    attachment=os.getcwd()+'/operation/attachments/'+file
                    file_=self.read_attachment(attachment)
                    message.attach(file_)
                    try:
                        server = smtplib.SMTP("smtp.gmail.com",port)
                        server.ehlo()
                        server.starttls()
                        server.login(self.sender_email,self.password)
                        server.sendmail(self.sender_email,self.receiver_email,message.as_string())
                        server.quit()
                        print("mail sent to %s %s"%(",".join(self.receiver_email),datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    except socket.error as e:
                        print("retrying........",type(e))
                        self.main()
                else:
                    print('csv file is empty and mail not sent........%s'%(datetime.now().strftime('%b %d, %Y')))        

