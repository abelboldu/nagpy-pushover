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

import sys

from nagpy.nagios import Nagios

class NagiosPlugin(Nagios):
    default_warn = '75'
    default_critical = '90'

    nagios_ok = 0
    nagios_warning = 1
    nagios_critical = 2
    nagios_unknown = 3
    nagios_dependent = 4

    def setupParser(self):
        p = Nagios.setupParser(self)
        p.add_option('-H', '--hostname', dest='host', 
                     default='localhost',
                     help='Host name of the db server')
        p.add_option('-w', '--warn', dest='warn', 
                     default=self.default_warn, 
                     help='Percentage at which to send a warning message')
        p.add_option('-c', '--critical', dest='crit', 
                     default=self.default_critical,
                     help='Percentage at which to send a critical message')
        return p

    def parseArgs(self):
        opts, args = Nagios.parseArgs(self)
        self.host = opts.host
        self.warn = float(opts.warn)
        self.crit = float(opts.crit)
        return opts, args

    def compare(self, low, high):
        res = float(low) / float(high) * 100
        if res < self.warn:
            return self.nagios_ok
        elif res >= self.warn and res < self.crit:
            return self.nagios_warning
        else:
            return self.nagios_critical
