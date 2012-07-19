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

from conary import dbstore

from nagpy.plugin import NagiosPlugin
from nagpy.util.exceptionHooks import stdout_hook

class checkDB(NagiosPlugin):
    def __init__(self):
        NagiosPlugin.__init__(self)
        self.dbErrorText = 'An error occured trying to check the db.'
        self.connection = dbstore.connect(self.getDbStoreConnectStr(),
                                          driver='mysql')
        self.cu = self.connection.cursor()

    def getDbStoreConnectStr(self):
        return "%s:%s@%s/%s" % (self.user, self.passwd, self.host, self.db)

    def setupParser(self):
        p = NagiosPlugin.setupParser(self)
        p.add_option('-u', '--username', dest='user',
                     help='User name of the db user')
        p.add_option('-p', '--password', dest='password',
                     help='Password of the db user')
        p.add_option('-d', '--database', dest='db',
                     help='Database to connect to')
        return p

    def parseArgs(self):
        opts, args = NagiosPlugin.parseArgs(self)
        if not opts.user:
            print "user name not defined"
            self.usage()
        elif not opts.password:
            print "password not defined"
            self.usage()
        elif not opts.db:
            print "database not defined"
            self.usage()
        self.user = opts.user
        self.passwd = opts.password
        self.db = opts.db
        return opts, args

    def getVar(self, table, var):
        try:
            self.cu.execute('show global %s where variable_name=?' % table, var)
            res = self.cu.fetchone()
            if len(res) == 2 and res[0] == var:
                return res[1]
            else:
                raise CheckDBError('','')
        except:
            raise CheckDBError(self.dbErrorText, 'UNKNOWN')

    def getDbVariable(self, var):
        return self.getVar('variables', var)

    def getDbStatus(self, var):
        return self.getVar('status', var)

    @stdout_hook
    def check(self, var1, var2):
        res1 = self.getDbVariable(var1)
        res2 = self.getDbStatus(var2)
        return self.compare(res2, res1), res2
