#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
	
def search(conn, filter, subtree=False):
	scope = ldap.SCOPE_ONELEVEL
	if (subtree):
		scope = ldap.SCOPE_SUBTREE
	return conn.search_s(config["basedn"], scope, filter)

def listdn(result):
	for r in result:
		if len(r[1]) == 1 and len(r[1][0]) > 4 and r[1][0][0:4] == "ldap": # skip referrals
			continue
		print r[0]

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

