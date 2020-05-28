import smtplib,ssl
import sys
import os
import socket,logging
import openpyxl as xl
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
        self.sheet_row=0
        self.sheets=["Movies,Series,Episodes"]

    def user_input(self):
        self.sender_email="saayan@headrun.com"
        self.receiver_email=["hott@headrun.com"]
        self.password="9891274567"

    def user_message(self):
        text="""Hi Team,


    Justwatch Keepup contents for the service HBOGO,Showtime,Hulu.
        
    Please find the attachment. 



    With best regards,
    Saayan Das,"""
    
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
        #import pdb;pdb.set_trace()
        self.user_input()
        message=MIMEMultipart("alternative")
        message["Subject"]="Justwatch Keepup Content on %s"%(datetime.now().strftime('%b %d, %Y'))
        message["From"]=self.sender_email
        message["To"]=",".join([email_id for email_id in self.receiver_email])
        port =587
        text=self.user_message()
        part1=MIMEText(text,"plain")
        message.attach(part1)
        filenames=['Justwatch_keepup_contents_%s.xlsx'%(datetime.now().strftime('%b %d, %Y'))]
        for file in filenames:
            attachment=os.getcwd()+'/operation/attachments/'+file
            wb = xl.load_workbook(attachment, enumerate)
            for sheet in self.sheets:
                sheet = wb.get_sheet_by_name('Movies')
                sheet = wb.worksheets[0]
                self.sheet_row+=sheet.max_row
            if self.sheet_row > 3 :            
                file_=self.read_attachment(attachment)
                message.attach(file_)
                try:
                    server = smtplib.SMTP("smtp.gmail.com",port)
                    server.ehlo()
                    server.starttls()
                    server.login(self.sender_email,self.password)
                    server.sendmail(self.sender_email,self.receiver_email,message.as_string())
                    server.quit()
                    logging.info("mail sent to %s %s"%(",".join(self.receiver_email),datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                except socket.error as e:
                    logging.info("retrying........",type(e))
                    self.main()
            else:
                logging.info("mail can't sent and excel file is empty............%s"%datetime.now().strftime("%Y-%m-%d %H:%M:%S"))        


