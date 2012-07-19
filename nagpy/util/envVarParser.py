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

import os

def readEnv():
    dict = {}
    for key, value in os.environ.iteritems():
        key = key.lower()
        if key.startswith('nagios_'):
            dict[key[7:]] = value
    return dict

def writeEnv(file):
    def envStr(var):
        return 'NAGIOS_%s' % var.upper()
    for line in file.split('\n'):
        sl = line.split()
        if sl == []: continue
        if len(sl) == 1:
            os.environ[envStr(sl[0])] = ''
            os.putenv(envStr(sl[0]), '')
        else:
            os.environ[envStr(sl[0])] = ' '.join(sl[1:])
            os.putenv(envStr(sl[0]), ' '.join(sl[1:]))
