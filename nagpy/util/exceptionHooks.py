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
import time
import traceback

from nagpy import errors
from nagpy.util import mail

def tb_info():
    exception, e, bt = sys.exc_info()
    info = {'error_name': exception.__name__,
            'error': e,
            'time': time.ctime(time.time()),
            'tb': ''.join(traceback.format_tb(bt))}
    body = """\
Unhandled exception from nagios:

Time of occurrence: %(time)s
%(error_name)s: %(error)s

%(tb)s""" % info
    return body

def stdout_hook(func):
    def wrapper(self, *args):
        try:
            return func(self, *args)
        except:
            print tb_info()
            sys.exit(self.nagios_unknown)
            #return self.nagios_unknown, tb_info()
    wrapper.__wrapped_func__ = func
    return wrapper

def email_hook(func):
    def wrapper(self, *args):
        try:
            return func(self, *args)
        except:
            if self.errorEmail:
                subject = "Nagios: Notification Error"
                mail.sendMail(self.errorEmail, 'Nagios', self.errorEmail, 
                              subject, tb_info())
            else:
                raise
    wrapper.__wrapped_func__ = func
    return wrapper

def ksockhook(func):
    def wrapper(self, *args):
        try:
            return func(self, *args)
        except:
            if self.socket:
                self.socket.close()
            raise
    wrapper.__wrapped_func__ = func
    return wrapper

def KibotOutputHandler(func):
    def wrapper(self, *args):
        res = func(self, *args)
        if res == 'OK':
            return res
        elif res.startswith('command not found'):
            raise errors.KibotCommandNotFoundError(res)
        else:
            raise errors.KibotError(res)
    wrapper.__wrapped_func__ = func
    return wrapper

def KibotModuleLoader(module):
    def deco(func):
        def wrapper(self, *args):
            default_modules = ['base', 'auth', 'irc']
            if module not in default_modules and module not in self._modules():
                self._loadModule(module)
            return func(self, *args) 
        wrapper.__wrapped_func__ = func
        return wrapper
    return deco
