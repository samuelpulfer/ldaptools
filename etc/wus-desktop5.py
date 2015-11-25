#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# log files
modification_logfile="var/modification.log"

# groups to sync
sync = [
	# Ärzte
	{
		"from": "(&(cn=MQ_ANA_LA)(objectClass=group))", 
		"to": "CN=MQ_B_U_Anaesthesiologie-Aerzte-LA,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch",
		"method": "sync", # sync|copy|delete
	},
	{
		"from": "(&(cn=MQ_ANA_OA)(objectClass=group))", 
		"to": "CN=MQ_B_U_Anaesthesiologie-Aerzte-OA,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch",
		"method": "sync", # sync|copy|delete
	},
	{
		"from": "(&(cn=MQ_ANA_AA)(objectClass=group))", 
		"to": "CN=MQ_B_U_Anaesthesiologie-Aerzte-AA,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch",
		"method": "sync", # sync|copy|delete
	},
	{
		"from": "(&(cn=MQ_ANA_OIB_Aerzte)(objectClass=group))", 
		"to": "CN=MQ_B_U_Anaesthesiologie-Aerzte-OIB,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch",
		"method": "sync", # sync|copy|delete
	},
	
	# Pflege
	{
		"from": "(&(cn=MQ_ANA_Pflege)(objectClass=group))", 
		"to": "CN=MQ_B_U_Anaesthesiologie-Pflege-ANA,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch",
		"method": "sync", # sync|copy|delete
	},
	{
		"from": "(&(cn=MQ_ANA_OIB_Pflege)(objectClass=group))", 
		"to": "CN=MQ_B_U_Anaesthesiologie-Pflege-OIB,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch",
		"method": "sync", # sync|copy|delete
	},
	{
		"from": "(&(cn=MQ_ANA_OPS)(objectClass=group))", 
		"to": "CN=MQ_B_U_Anaesthesiologie-Pflege-OPS,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch",
		"method": "sync", # sync|copy|delete
	},
	
	# Admin
	{
		"from": "(&(cn=MQ_ANA_IT)(objectClass=group))", 
		"to": "CN=MQ_B_U_Anaesthesiologie-Admin-IT,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch",
		"method": "sync", # sync|copy|delete
	},
	{
		"from": "(&(cn=MQ_ANA_SEK)(objectClass=group))", 
		"to": "CN=MQ_B_U_Anaesthesiologie-Admin-Sek,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch",
		"method": "sync", # sync|copy|delete
	},
	


]

"""
	{
		"from": "CN=MQ_ANA_LA,OU=Exchange_Adressbuecher,OU=PITServer,DC=ms,DC=uhbs,DC=ch", 
		"to": "CN=MQ_B_U_Anaesthesiologie-Aerzte-LA,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch"
	},
	{
		"from": "CN=MQ_ANA_OA,OU=Exchange_Adressbuecher,OU=PITServer,DC=ms,DC=uhbs,DC=ch", 
		"to": "CN=MQ_B_U_Anaesthesiologie-Aerzte-OA,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch"
	},
	{
		"from": "CN=MQ_ANA_AA,OU=Exchange_Adressbuecher,OU=PITServer,DC=ms,DC=uhbs,DC=ch", 
		"to": "CN=MQ_B_U_Anaesthesiologie-Aerzte-AA,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch"
	},
"""

userdn = "CN=A_WunderlinS,OU=Admin,OU=Users,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch"
userpw = None # stored in etc/`hostname`.pass

# Domain infos
baseDN = "dc=ms,dc=uhbs,dc=ch"
ldap_url = "ldap://ms.uhbs.ch:389"	

