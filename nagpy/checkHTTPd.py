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

import urlgrabber

from nagpy.plugin import NagiosPlugin
from nagpy.util.exceptionHooks import stdout_hook

class CheckHTTPd(NagiosPlugin):
    def setupParser(self):
        p = NagiosPlugin.setupParser(self)
        p.add_option('-u', '--url', dest='url',
                     help='URL for page to parse')
        return p

    def parseArgs(self):
        opts, args = NagiosPlugin.parseArgs(self)
        if not opts.url:
            print "URL not defined"
            self.usage()
        if not opts.host or opts.host is 'localhost':
            print "Host not defined"
            self.usage()
        self.url = opts.url
        return opts, args

    @stdout_hook
    def check(self):
        page = urlgrabber.urlread(self.formatURL())
        return self.parsePage(page)

    def formatURL(self):
        return 'http://%s/%s' % (self.host, self.url)

    def parsePage(self, page):
        return {}
