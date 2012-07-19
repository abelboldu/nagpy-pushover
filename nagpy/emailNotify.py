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

from nagpy.util import mail
from nagpy.util.exceptionHooks import email_hook
from nagpy.errors import MailError
from nagpy.notify import NagiosNotification

class EmailNotification(NagiosNotification):
    template = ''
    subject_template = ''

    def setupParser(self):
        p = NagiosNotification.setupParser(self)
        p.add_option('-d', '--dest-email', dest='emailAddr', 
                     help='email address to send to')
        p.add_option('-f', '--from-email', dest='fromEmail',
                     help='email address to send from')
        p.add_option('-n', '--from-name', dest='fromName',
                     help='name to send email from')
        p.add_option('-e', '--error-email', dest='errorEmail', 
                     default='root@localhost', 
                     help='email address to send errors to')
        return p

    def parseArgs(self):
        opts, args = NagiosNotification.parseArgs(self)
        if not opts.fromEmail:
            print "Source email address not defined."
            self.usage()
        if not opts.fromName:
            print "Name to send email from not defined."
            self.usage()
        if opts.emailAddr:
            self.emailAddr = opts.emailAddr
        elif self.vars['contactemail'] != '':
            self.emailAddr = self.vars['contactemail']
        else:
            print "Contact email not defined."
            self.usage()
        self.fromEmail = opts.fromEmail
        self.fromName = opts.fromName
        self.errorEmail = opts.errorEmail
        return opts, args

    def send(self, subject, body):
        try:
            mail.sendMailWithChecks(self.fromEmail, self.fromName,
                                    self.emailAddr, subject, body)
        except MailError, e:
            body = 'To Address: %s\nError: %s\n\n%s' % (self.emailAddr, 
                                                        e.error, body)
            mail.sendMailWithChecks(self.fromEmail, self.fromName, 
                                    self.errorEmail, subject, body)

    @email_hook
    def notify(self):
        NagiosNotification.notify(self)
        subject = self.subject_template % self.vars
        body = self.template % self.vars
        self.send(subject, body)


class HostNotifyShort(EmailNotification):
    template = """

Info: %(hostoutput)s
Time: %(date)s %(time)s
Type: %(notificationtype)s
"""
    subject_template = """%(hoststate)s: %(hostname)s"""


class HostNotifyLong(HostNotifyShort):
    template = "** Nagios Host Notification **" + HostNotifyShort.template + """
Host: %(hostname)s
Address: %(hostaddress)s
State: %(hoststate)s

Acknowledgment Author: %(hostackauthor)s
ACknowledgment: %(hostackcomment)s

Check Command: %(hostcheckcommand)s
Latency: %(hostlatency)s
Group: %(hostgroupname)s
Downtime: %(hostdowntime)s
Duration: %(hostduration)s

Perf Data: %(hostperfdata)s
"""


class ServiceNotifyShort(EmailNotification):
    template = """

Info: %(serviceoutput)s
Time: %(date)s %(time)s
Type: %(notificationtype)s
"""
    subject_template = """%(servicestate)s: %(hostname)s"""


class ServiceNotifyLong(ServiceNotifyShort):
    template = "** Nagios Service Notification **" + ServiceNotifyShort.template + """
Host: %(hostname)s
Address: %(hostaddress)s
State: %(servicestate)s

Acknowledgment Author: %(serviceackauthor)s
Acknowledgment: %(serviceackcomment)s

Check Command: %(servicecheckcommand)s
Latency: %(servicelatency)s
Group: %(hostgroupname)s
Downtime: %(servicedowntime)s
Duration: %(serviceduration)s

Perf Data: %(serviceperfdata)s
"""
