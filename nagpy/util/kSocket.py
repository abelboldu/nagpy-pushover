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

import socket
from telnetlib import Telnet
from nagpy.errors import KSocketError

ksock = None

class KSocket(Telnet):
    def open(self, host, port=0):
        self.eof = 0
        self.host = host
        self.port = port
        msg = "getaddrinfo returns an empty list"
        try:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.sock.connect(host)
        except socket.error, msg:
            if self.sock:
                self.sock.close()
            self.sock = None
            raise KSocketError(msg)


def open(file):
    global ksock
    if not ksock:
        if ':' in file:
            host, port = file.split(':')
            ksock = Telnet(host, port)
        else:
            ksock = KSocket(file)
    return ksock
