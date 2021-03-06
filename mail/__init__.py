import smtplib
import config
from email.mime.text import MIMEText
from email.header import Header

class Mail(object):
    def __init__(self,mail_host='',mail_username='',mail_password=''):
        self.mail_host = mail_host
        self.mail_username = mail_username
        self.mail_password = mail_password

    def send(self,to_msg,to_add):
        sender = self.mail_username
        receivers = [to_add]
        conten = to_msg
        message = MIMEText(conten, 'plain', 'utf-8')
        message['To'] = to_add
        subject = '有一条薅羊毛告警，赶紧查看一下'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP_SSL(host=self.mail_host)
            smtpObj.connect(host=self.mail_host,port=465)
            smtpObj.login(self.mail_username, self.mail_password)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件" + e.strerror)

