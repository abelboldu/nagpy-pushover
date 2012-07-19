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

from nagpy.errors import KibotError
from nagpy.util import kSocket
from nagpy.util.exceptionHooks import ksockhook
from nagpy.util.exceptionHooks import KibotModuleLoader as moduleLoader
from nagpy.util.exceptionHooks import KibotOutputHandler as outputparser

class KBuffer(object):
    def __init__(self):
        self.buf = []
        self.finished_last_line = True
    def push(self, str, end=True):
        if not self.finished_last_line:
            self.buf[-1] += str
        self.buf.append(str)
        self.finished_last_line = end
    def pop(self):
        if len(self.buf) > 1 or (len(self.buf) == 1 and self.finished_last_line):
            return self.buf.pop(0)
        else:
            return None

class Kibot(object):
    def __init__(self, socket):
        self.socket_file = socket
        self.readbuffer = KBuffer()
        self.socket = kSocket.open(self.socket_file)

    @ksockhook
    def _send(self, str):
        self.socket.write('%s\n' % str)

    @ksockhook
    def _read(self):
        def formatLine(line):
            return ':'.join(line.split(':')[1:])
        try:
            line = self.socket.read_until('\n', 1)
            self.readbuffer.push(formatLine(line).strip())
        except EOFError, e: pass # disconect from remote
        return self.readbuffer.pop()

    def _modules(self):
        list = []
        self._send('help modules')
        self._read() # remove fist line of help message
        res = self._read()
        while res:
            list.append(res.split()[0])
            res = self._read()
        return list

    def _loadModule(self, module):
        self._send('load %s' % module)
        res = self._read()
        if res.startswith(module):
            return res
        else:
            raise KibotError(res)

    @outputparser
    @moduleLoader('irc')
    def inchan(self, chan, cmd):
        self._send('inchan %s %s' % (chan, cmd))
        return self._read()
