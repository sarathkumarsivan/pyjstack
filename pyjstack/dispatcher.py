#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Sarath Kumar Sivan, https://github.com/sarathkumarsivan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path


def connect(smtp_server, smtp_port, email, password):
    """
    Connect to the SMTP server to send emails.

    :param smtp_server: Hostname or IP Address of the SMTP server
    :param smtp_port: Port number of the SMTP server.
    :param email: Valid email address for authentication.
    :param password: Password of the email address for authentication.
    :returns: server instance after login with the credentials.
    :raises: None
    """
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email, password)
    return server


def connect(smtp_server, smtp_port=25):
    """
    Connect to the SMTP server to send emails.

    :param smtp_server: Hostname or IP Address of the SMTP server
    :param smtp_port: Port number of the SMTP server, default is 25.
    :returns: server instance without logging in.
    :raises: None
    """
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    return server


def attach(path):
    """
    Attach the given file to the email payload. The file size of the given 
    attachment should be less than or equal to the mazimum allowed size.

    :param path: File path of the attachment.
    :returns: None
    :raises: None
    """
    filename = os.path.basename(path)
    attachment = open(path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)


def send(server, from_email, to_email, subject, content, attachment):
    """
    Send the email with the provided options.

    :param server: SMTP server instance with starttls enabled.
    :param from_email: From email address for sending email message.
    :param to_email: To email addresses for sending email message.
    :param subject: Subject line of the email message.
    :param content: Message body of the email message.
    :param attachment: Attachment to be attached with the email message.
    :returns: None
    :raises: None
    """
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(content, 'html'))
    message.attach(attachment)
    server.sendmail(from_email, to_email, message.as_string()) 
    server.quit()


def send(smtp_server, smtp_port, from_email, password, to_email, subject, content, attachment):
    """
    Send the email with the provided options.

    :param smtp_server: Hostname or IP Adrress of the SMTP server.
    :param smtp_port: SMTP port number to send email message.
    :param from_email: From email address for sending email message.
    :param password: Password for SMTP authentication.
    :param to_email: To email addresses for sending email message.
    :param subject: Subject line of the email message.
    :param content: Message body of the email message.
    :param attachment: Attachment to be attached with the email message.
    :returns: None
    :raises: None
    """
    server = connect(smtp_server, smtp_port, from_email, password)
    send(server, from_email, to_email, subject, content, attachment)


def send(smtp_server, smtp_port, from_email, to_email, subject, content, attachment):
    """
    Send the email with the provided options.

    :param smtp_server: Hostname or IP Adrress of the SMTP server.
    :param smtp_port: SMTP port number to send email message.
    :param from_email: From email address for sending email message.
    :param to_email: To email addresses for sending email message.
    :param subject: Subject line of the email message.
    :param content: Message body of the email message.
    :param attachment: Attachment to be attached with the email message.
    :returns: None
    :raises: None
    """
    server = connect(smtp_server, smtp_port)
    send(server, from_email, to_email, subject, content, attachment)