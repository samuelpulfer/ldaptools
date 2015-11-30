#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
This is an example configuration file. Use it as template. You will have to 
copy it to `hostname`.py in the same folder. Hostname refers to the output 
of the hostname command.

The password is read from the `hostname`.pass file. You must create this file.
Simply use any text editor and create a file containing the password (and only 
the password) and protect it with proper filesystem permissions (chmod 600).
"""

# log files
modification_logfile="var/modification.log"

# groups to sync
sync = [
	{
		# valid ldap query. members of all returned groups are copied to target
		"from": "(&(cn=groupName)(objectClass=group))",
		# destination dn, this object's members will be propulated
		"to": "CN=TgtGroup,DC=Users,DC=example,DC=com",
		"method": "sync", # sync|copy|delete
	}, # etc 
]

sync_vd = [
	{
		"filter": "(& (cn=my_group) (objectClass=group) )", 
		"to": "CN=DC=example,DC=com"}
	},
]

userdn = "CN=admin,DC=example,DC=com"
userpw = None

# Domain infos
baseDN = "DC=example,DC=com"
ldap_url = "ldap://example.com:389"	

