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

python_files = 

extra_dist = \
	Makefile \
	check_httpd_threads \
	check_mysql_threads

dist_files = $(python_files) $(extra_dist)

SUBDIRS	= 

all: default-subdirs default-all

install-mkdirs:
	mkdir -p $(DESTDIR)$(libexecdir)

install: install-mkdirs
	install -m 755 check_httpd_threads $(DESTDIR)$(libexecdir)
	install -m 755 check_mysql_threads $(DESTDIR)$(libexecdir)

dist: default-dist

clean: default-clean

include ../Make.rules
