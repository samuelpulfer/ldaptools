#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# log files
modification_logfile="var/modification.log"

# groups to sync
sync = [
	{
		"from": "(&(cn=MQ_ANA_LA)(objectClass=group))", 
		"to": "CN=MQ_B_M_Anaesthesiologie-VD-User-Aerzte-LA,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch"
	}
]
"""
	{
		"from": "CN=MQ_ANA_LA,OU=Exchange_Adressbuecher,OU=PITServer,DC=ms,DC=uhbs,DC=ch", 
		"to": "CN=MQ_B_M_Anaesthesiologie-VD-User-Aerzte-LA,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch"
	},
	{
		"from": "CN=MQ_ANA_OA,OU=Exchange_Adressbuecher,OU=PITServer,DC=ms,DC=uhbs,DC=ch", 
		"to": "CN=MQ_B_M_Anaesthesiologie-VD-User-Aerzte-OA,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch"
	},
	{
		"from": "CN=MQ_ANA_AA,OU=Exchange_Adressbuecher,OU=PITServer,DC=ms,DC=uhbs,DC=ch", 
		"to": "CN=MQ_B_M_Anaesthesiologie-VD-User-Aerzte-AA,OU=Business,OU=Groups,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch"
	},
"""

userdn = "CN=A_WunderlinS,OU=Admin,OU=Users,OU=MQInf,OU=USB,DC=ms,DC=uhbs,DC=ch"
userpw = None

# Domain infos
baseDN = "dc=ms,dc=uhbs,dc=ch"
ldap_url = "ldap://ms.uhbs.ch:389"	

