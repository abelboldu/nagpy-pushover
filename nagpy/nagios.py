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
import optparse

from nagpy.constants import *

class Nagios(object):
    def __init__(self):
        self.version = version

        self.parser = self.setupParser()
        self.parseArgs()

    def usage(self):
        self.parser.print_help()
        sys.exit(1)

    def setupParser(self):
        p = optparse.OptionParser()
        p.add_option('-V', '--version', action='store_true', dest='version',
                     help='print version')
        p.add_option('-v', '--verbose', action='store_true', dest='verbose',
                     help='make louder')
        p.add_option('-q', '--quiet', action='store_false', dest='verbose',
                     help='make quieter')
        return p

    def parseArgs(self):
        opts, args = self.parser.parse_args()
        if opts.version:
            print "%s version %s" % (sys.argv[0], self.version)
            sys.exit(0)
        if opts.verbose:
            self.verbose = True
        else:
            self.verbose = False
        return opts, args

    def dict2str(self, d):
        ret = ''
        spaces = 40
        keys = d.keys()
        keys.sort()
        for key in keys:
            ret += '%s' % key
            if d[key] != '':
                for i in range(spaces - len(key)):
                    ret += ' '
                ret += '%s' % d[key]
            ret += '\n'
        return ret
