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

from nagpy.nagios import Nagios
from nagpy.util.envVarParser import readEnv

class NagiosNotification(Nagios):
    def __init__(self):
        Nagios.__init__(self)
        self.vars = readEnv()

    def varsToString(self):
        return self.dict2str(self.vars)

    def notify(self):
        pass
