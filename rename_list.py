#! /usr/bin/python
#
# Copyright (C) 2001,2002 by the Free Software Foundation, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

"""Rename list.

Usage: %(PROGRAM) [options] oldlistname newlistname 

Options:
    -v / --verbose
        Print what the script is doing.

Note that listnames are forced to lowercase.
"""

import sys
import os
import getopt
import ntpath

import paths
from Mailman import mm_cfg
from Mailman import MailList
from Mailman import Site
from Mailman import Utils

PROGRAM = sys.argv[0]


def usage(code, msg=''):
    if code:
        fd = sys.stderr
    else:
        fd = sys.stdout
    print >> fd, __doc__
    if msg:
        print >> fd, msg
    sys.exit(code)


def aliases_entries(listname):
    print
    print '# Distribution list %s' % listname 
    print '%s:             "|/var/lib/mailman/mail/mailman post %s' % (listname, listname)
    print '%s-admin:       "|/var/lib/mailman/mail/mailman admin %s' % (listname, listname)
    print '%s-bounces:     "|/var/lib/mailman/mail/mailman bounces %s' % (listname, listname)
    print '%s-confirm:     "|/var/lib/mailman/mail/mailman confirm %s' % (listname, listname)
    print '%s-join:        "|/var/lib/mailman/mail/mailman join %s' % (listname, listname)
    print '%s-leave:       "|/var/lib/mailman/mail/mailman leave %s' % (listname, listname)
    print '%s-owner:       "|/var/lib/mailman/mail/mailman owner %s' % (listname, listname)
    print '%s-request:     "|/var/lib/mailman/mail/mailman request %s' % (listname, listname)
    print '%s-subscribe:   "|/var/lib/mailman/mail/mailman subscribe %s' % (listname, listname)
    print '%s-unsubscribe: "|/var/lib/mailman/mail/mailman unsubscribe %s' % (listname, listname)
    print

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vh:', ['verbose', 'help'])
    except getopt.error, msg:
        usage(1, msg)

    verbose = 0
    for opt, arg in opts:
        if opt in ('-h', '--help'):
	    usage(0)
        if opt in ('-v', '--verbose'):
            verbose = 1


    if len(args) > 1:
        oldlistname = args[0].lower()
	newlistname = args[1].lower()
    else:
        print >> sys.stderr, 'No list names given'
	print >> sys.stderr, "Try '%s --help' for more information." % PROGRAM
	return

    if not Utils.list_exists(oldlistname):
            usage(1, "List '%s' not exists." % (oldlistname))

    if Utils.list_exists(newlistname):
            usage(1, "List '%s' already exists." % (newlistname))

    if verbose:
        print 'Renaming list %s to %s.' % (oldlistname, newlistname)

    #mlist = MailList.MailList()
    #mlist.Lock()
    
    oldlistpath = Site.get_listpath(oldlistname)
    lists_path = os.path.dirname(oldlistpath)
    newlistpath = lists_path + '/' + newlistname


    #print 'oldlistpath: %s' % (oldlistpath)
    #print 'list path: %s' % (lists_path)
    #print 'newlistpath: %s' % (newlistpath)

    # Goyo: descomentar
    os.rename(oldlistpath, newlistpath)
    

    if verbose:
        print 'Assing archives of list %s to %s.' % (oldlistname, newlistname)
  
    oldarchdir = Site.get_archpath(oldlistname)
    arch_dir = os.path.dirname(oldarchdir)
    newarchdir = arch_dir + '/' + newlistname

    oldmbox = arch_dir + '/' + oldlistname + '.mbox'
    newmbox = arch_dir + '/' + newlistname + '.mbox'

    oldmbox_mbox = newmbox + '/' + oldlistname + '.mbox'
    newmbox_mbox = newmbox + '/' + newlistname + '.mbox'
  
    #print 'old archive => %s' % (oldarchdir)    
    #print 'new archive => %s' % (newarchdir)    

    #print 'old mbox => %s' % (oldmbox)    
    #print 'new mbox => %s' % (newmbox)    
   
    #print 'old mbox_mbox => %s' % (oldmbox_mbox)    
    #print 'new mbox_mbox => %s' % (newmbox_mbox)    

    # Goyo: descomentar
    os.rename(oldarchdir, newarchdir)
    os.rename(oldmbox, newmbox)
    os.rename(oldmbox_mbox, newmbox_mbox)
   
    os.system("arch -wipe %s" % (newlistname))

    print 'Now change aliases file ...'
    print

    aliases_entries(oldlistname)

    print '... per ..'

    aliases_entries(newlistname)

if __name__ == '__main__':
    main()
