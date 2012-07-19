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

class NagPyError(Exception):
    def __init__(self, error=None):
        self.error = error
    def __repr__(self):
        if self.error:
            return self.error
        else:
            return ''
    __str__ = __repr__

class NagiosPluginError(NagPyError):
    def __init__(self, error, state):
        self.error = error
        self.state = state
    def __repr__(self):
        return '%s: %s' % (state, error)

class CheckDBError(NagiosPluginError):
    pass

class CheckHTTPdError(NagiosPluginError):
    pass

class NotificationError(NagPyError):
    pass

class UtilError(NagPyError):
    pass

class MailError(UtilError):
    error="there was a problem sending mail"

class KSocketError(UtilError):
    pass

class KibotError(UtilError):
    pass

class KibotCommandNotFoundError(KibotError):
    pass
