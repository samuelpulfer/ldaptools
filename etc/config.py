#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os

# log files
modification_logfile="var/modification.log"

# groups to sync
sync = [
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
]

userdn = "CN=Medizintechnik Testaccount,OU=Admin,OU=Users,OU=MTInf,OU=USB,DC=ms,DC=uhbs,DC=ch"
_pwfile = os.path.realpath(__file__)) + "/" + 'user.pass'
with open(os.path.dirname(_pwfile) as f: 
	userpw = f.read()
except IOError:
	print('Please create the password file ' + _pwfile)

# Domain infos
baseDN = "ou=USB,dc=ms,dc=uhbs,dc=ch"
host = "ms.uhbs.ch"
ldap_url = "ldap://ms.uhbs.ch:389"	

