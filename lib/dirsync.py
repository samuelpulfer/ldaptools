#!/usr/bin/env python
# -*- coding: utf8 -*-

""" Toolset for synchronizing directory groups via ldap """

# setup paths
import os, sys
import ldap
import ldap.modlist as modlist
import logging
import ldap.filter
import re

## global variables ############################################################

def member_delete(ldapconn, target_group):
	""" delete all "member" attributes of a node
	
	    it expects the following parameters
	    - ldapconn: an ldap connection object
	    - target_group: DN of the target
	"""
	pass

def member_copy(ldapconn, cnlist, target_group, src_attr="member", tgt_attr="member"):
	""" this methods copies members from one group to another. 
	    
	    member in the target group which are not in the src group will remain in the target grp.
	    
	    it expects the following parameters
	    - ldapconn: an ldap connection object
	    - cnlist: list of DNs of new members
	    - target_group: DN of the target
	    
	    Both objects (src, tgt) must be able to have one to many "member" attributes.
	"""
	
	# get target group
	r = get_one(ldapconn, target_group)
	
	# extract existing members
	res = r[0][1]
	if src_attr not in res:
		tgt_list = []
	else:
		tgt_list = res[src_attr]
	
	ret = {
		"method": "copy",
		"old_length": len(tgt_list),
		"new_length": 0,
		"added": 0
	}
	
	#print tgt_list
	
	# append existing members to new members
	new_member = tgt_list[:] # copy rather than reference
	for e in cnlist:
		if e not in new_member:
			new_member.append(e)
			ret["added"] += 1
	
	# create mod list
	mlist = modlist.modifyModlist({tgt_attr: tgt_list}, {tgt_attr: new_member})
	
	# commit if the modlist is not empty
	ret["new_length"] = ret["old_length"]
	if len(mlist) > 0:
		#print mlist
		if mlist[0][0] == 1:
			ret["new_length"] = len(mlist[1][2])
		else:
			ret["new_length"] = len(mlist[0][2])
			
		ldapconn.modify_s(target_group, mlist)
	
	return ret
	
def member_sync(ldapconn, cnlist, target_group, preserveGroupMemebers=True, src_attr="member", tgt_attr="member"):
	""" this methods syncs members from one group to another. 
	    
	    member in the target group which are not in the src group will be removed. 
	    
	    it expects the following parameters
	    - ldapconn: an ldap connection object
	    - cnlist: list of DNs of new members
	    - target_group: DN of the target
	    - preserveGroupMemebers: keep all members that have an objectClass == 'group'
	    
	    Both objects (src, tgt) must be able to have one to many "member" attributes.
	"""
	
	# get target group
	r = get_one(ldapconn, target_group)
	
	# extract existing members
	res = r[0][1]
	if src_attr not in res:
		tgt_list = []
	else:
		tgt_list = res[src_attr]
	
	ret = {
		"method": "sync",
		"old_length": len(tgt_list),
		"new_length": len(cnlist)
	}

	# find members that are group
	grp_member = []
	if preserveGroupMemebers:
		for e in tgt_list:
			o = get_one(ldapconn, e)
			is_group = False
			try:
				is_group = ("group" in o[0][1]["objectClass"])
			except:
				pass
			#print is_group, o[0][0]
			
			if is_group:
				grp_member.append(o[0][0])
	
	cnlist = cnlist + grp_member
	
	# create mod list
	mlist = modlist.modifyModlist({tgt_attr: tgt_list}, {tgt_attr: cnlist})
	
	# commit if the modlist is not empty
	ret["new_length"] = ret["old_length"]
	if len(mlist) > 0:
		#print mlist
		if mlist[0][0] == 1:
			ret["new_length"] = len(mlist[1][2])
		else:
			ret["new_length"] = len(mlist[0][2])
		
		ldapconn.modify_s(target_group, mlist)
	
	return ret

def get_one(ldapconn, dn):
	""" fetch a single object from a directory by DN 
	
	This method hacks around silly CN's that use characers like "(),\" in the name
	
	"""
	parts = dn.split(",")
	cn = parts[0]
	#search = ",".join(parts[1:])
	
	# this hack is required because our super directory 
	# architects put () and , into the DN
	f = re.sub(r'([^\\]),.*', "\\1", dn)
	search = dn.replace(f+",", "").strip()
	f = f.replace("\\,", ",")
	f = ldap.filter.escape_filter_chars(f, 0);
	return ldapconn.search_s(search, ldap.SCOPE_ONELEVEL, f)

