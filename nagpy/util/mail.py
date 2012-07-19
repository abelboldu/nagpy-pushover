#
# Copyright (c) 2006 rPath, Inc.
#
# This program is distributed under the terms of the Common Public License,
# version 1.0. A copy of this license should have been distributed with this
# source file in a file called LICENSE. If it is not present, the license
# is always available at http://www.opensource.org/licenses/cpl.php.
#
# This program is distributed in the hope that it will be useful, but
# without any waranty; without even the implied warranty of merchantability
# or fitness for a particular purpose. See the Common Public License for
# full details.
#

import socket
import smtplib
import dns.resolver
from email import MIMEText

from nagpy.errors import MailError

def digMX(hostname):
    try:
        answers = dns.resolver.query(hostname, 'MX')
    except dns.resolver.NoAnswer:
        return None
    return answers

def sendMailWithChecks(fromEmail, fromEmailName, toEmail, subject, body):
    validateEmailDomain(toEmail)
    try:
        sendMail(fromEmail, fromEmailName, toEmail, subject, body)
    except smtplib.SMTPRecipientsRefused:
        raise MailError("Email could not be sent: Recipient refused by server.")

def validateEmailDomain(toEmail):
    toDomain = smtplib.quoteaddr(toEmail).split('@')[-1][0:-1]
    VALIDATED_DOMAINS = ('localhost', 'localhost.localdomain')
    # basically if we don't implicitly know this domain,
    # and we can't look up the DNS entry of the MX
    # use gethostbyname to validate the email address
    try:
        if not ((toDomain in VALIDATED_DOMAINS) or digMX(toDomain)):
            socket.gethostbyname(toDomain)
    except (socket.gaierror, dns.resolver.NXDOMAIN):
        raise MailError("Email could not be sent: Bad domain name.")

def sendMail(fromEmail, fromEmailName, toEmail, subject, body):
    msg = MIMEText.MIMEText(str(body))
    msg['Subject'] = subject
    msg['From'] = '"%s" <%s>' % (fromEmailName, fromEmail)
    msg['To'] = toEmail

    s = smtplib.SMTP()
    s.connect()
    s.sendmail(fromEmail, [toEmail], msg.as_string())
    s.close()
