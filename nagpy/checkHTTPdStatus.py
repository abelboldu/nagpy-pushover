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

from nagpy.checkHTTPd import CheckHTTPd
from nagpy.errors import CheckHTTPdError

class CheckHTTPdStatus(CheckHTTPd):
    def formatURL(self):
        return '%s/?auto' % CheckHTTPd.formatURL(self)

    def parsePage(self, page):
        """
        "_" => 0,   # waiting
        "S" => 0,   # starting up
        "R" => 0,   # reading request
        "W" => 0,   # sending reply
        "K" => 0,   # keepalive
        "D" => 0,   # DNS lookup
        "C" => 0,   # closing connection
        "L" => 0,   # logging
        "G" => 0,   # graceful finishing
        "I" => 0,   # idle cleanup
        "." => 0    # open slot
        """

        stat = {'Waiting': 0, 'Starting': 0, 'Reading': 0, 'Sending': 0,
                'Keepalive': 0, 'Dnslookup': 0, 'Closing': 0, 'Logging': 0,
                'Gracefull_finishing': 0, 'Idle_cleanup': 0, 'Open_slot': 0,
                'Total': 0}

        for line in page.split('\n'):
            l = line.split(':')
            if len(l) != 2: continue
            stat[l[0]] = l[1].strip()

        for char in stat['Scoreboard']:
            stat['Total'] += 1
            if char is '_': stat['Waiting'] += 1
            elif char is 'S': stat['Starting'] += 1
            elif char is 'R': stat['Reading'] += 1
            elif char is 'W': stat['Sending'] += 1
            elif char is 'K': stat['Keepalive'] += 1
            elif char is 'D': stat['Dnslookup'] += 1
            elif char is 'C': stat['Closing'] += 1
            elif char is 'L': stat['Logging'] += 1
            elif char is 'G': stat['Gracefull_finishing'] += 1
            elif char is 'I': stat['Idle_cleanup'] += 1
            elif char is '.': stat['Open_slot'] += 1
            else: raise CheckHTTPdError, "Invalid scorboard type: %s" % char

        return stat
