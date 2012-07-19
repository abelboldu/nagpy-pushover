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

extra_dist = Makefile \
    nagios_test_email_notify \
    nagios_long_host_email_notify \
    nagios_long_service_email_notify \
    nagios_short_host_email_notify \
    nagios_short_service_email_notify \
    nagios_host_kibot_notify \
    nagios_service_kibot_notify

dist_files = $(python_files) $(extra_dist)

SUBDIRS	= 

all: default-subdirs default-all

install-mkdirs:
	mkdir -p $(DESTDIR)$(bindir)

install: install-mkdirs
	install -m 755 nagios_test_email_notify $(DESTDIR)$(bindir)
	install -m 755 nagios_long_host_email_notify $(DESTDIR)$(bindir)
	install -m 755 nagios_long_service_email_notify $(DESTDIR)$(bindir)
	install -m 755 nagios_short_host_email_notify $(DESTDIR)$(bindir)
	install -m 755 nagios_short_service_email_notify $(DESTDIR)$(bindir)
	install -m 755 nagios_host_kibot_notify $(DESTDIR)$(bindir)
	install -m 755 nagios_service_kibot_notify $(DESTDIR)$(bindir)

dist: default-dist

clean: default-clean

include ../Make.rules
