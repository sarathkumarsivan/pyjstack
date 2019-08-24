import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

def connect(smtp_server, smtp_port, email, password):
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email, password)
    return server

def connect(smtp_server, smtp_port=25):
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    return server

def attach(path):
    filename = os.path.basename(path)
    attachment = open(path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

def send(server, from_email, to_email, subject, content, attachment):
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    message.attach(MIMEText(content, 'html'))
    message.attach(attachment)

    server.sendmail(from_email, to_email, message.as_string()) 
    server.quit()

def send(smtp_server, smtp_port, from_email, password, to_email, subject, content, attachment):
    server = connect(smtp_server, smtp_port, from_email, password)
    send(server, from_email, to_email, subject, content, attachment)