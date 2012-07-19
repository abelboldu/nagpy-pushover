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

import nagpy.emailNotify
from nagpy.util.kibot import Kibot
from nagpy.notify import NagiosNotification
from nagpy.util.exceptionHooks import email_hook

class KibotNotify(NagiosNotification):
    template = ''

    def setupParser(self):
        p = NagiosNotification.setupParser(self)
        p.add_option('-s', '--socket', dest='socket',
                     help='path to kibot socket')
        p.add_option('-c', '--channel', dest='channel',
                     help='channel to send notification on')
        p.add_option('-e', '--error', dest='errorEmail',
                     help='email to send tracebacks to')
        return p

    def parseArgs(self):
        opts, args = NagiosNotification.parseArgs(self)
        if not opts.socket:
            print "Socket not defined."
            self.usage()
        if not opts.channel:
            print "Channel not defined."
            self.usage()
        self.bot = Kibot(opts.socket)
        self.channel = opts.channel
        self.errorEmail = opts.errorEmail
        return opts, args

    @email_hook
    def notify(self):
        NagiosNotification.notify(self)
        msg = []
        for line in (self.template % self.vars).split('\n'):
            if not line == '' and not line.strip().endswith(':'):
                msg.append(line)
        self.bot.inchan(self.channel, 'say %s' % ', '.join(msg))


class HostNotify(KibotNotify):
    template = nagpy.emailNotify.HostNotifyLong.template

class ServiceNotify(KibotNotify):
    template = nagpy.emailNotify.ServiceNotifyLong.template
