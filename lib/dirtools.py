#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" ldap basic utilities

- connect
- disconnect
- search: search directory
- len: length of search result
- listdn: list DN's of a result (for debugging)
"""

import sys, os
import socket
import ldap

# module variables
_conn = None

def disconnect():
	global _conn
	_conn.unbind_s()

def connect(uri, binddn, userpw):
	global _conn
	
	if _conn != None:
		return _conn
	
	_conn = ldap.initialize(uri)
	_conn.protocol_version = ldap.VERSION3
	_conn.set_option(ldap.OPT_REFERRALS,0) # prevent bug in AD when searching basedn
	_conn.simple_bind_s(binddn, userpw)
	
	#print _conn
	return _conn
	
def search(filter, basedn, subtree=False):
	scope = ldap.SCOPE_ONELEVEL
	if (subtree):
		scope = ldap.SCOPE_SUBTREE
	return _conn.search_s(basedn, scope, filter)

def listdn(result):
	for r in result:
		if len(r[1]) == 1 and len(r[1][0]) > 4 and r[1][0][0:4] == "ldap": # skip referrals
			continue
		print r[0]

def len(result):
	""" Get length of Result (filtering invalid entries)
	
	LDAP results contain entries with empty DNs, at least this is what 
	Microsoft's AD returns. These empty entries are ldap urls pointing to 
	other directory trees. This is obsolete as of LDAPv3, so we ignore them.
	"""
	l = 0;
	for (dn, item) in result:
		if dn == None :
			continue
		l += 1
	return l

def test(argv):
	#init() # FIXME, this method moved to the main function of the program
	conn = connect(argv[1], argv[2], argv[3])
	filter = "(|(objectClass=group)(objectClass=posixGroup)(objectClass=organizationalUnit))"
	res  = search(conn, filter)
	listdn(res)
	disconnect()
	

if __name__ == "__main__":
	""" usage: dirtools.py [ldapuri] [binddn] [password] """
	test(sys.argv)

