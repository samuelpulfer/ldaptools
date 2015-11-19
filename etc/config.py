#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# NOTE: take care to keep the syntax bash compatible
#

# log files
modification_logfile="var/modification.log"

# groups to sync
syncfromcn="MT_B_Testgruppe"
synctocn="MT_B_Testgruppe2"

userdn = "CN=Medizintechnik Testaccount,OU=Admin,OU=Users,OU=MTInf,OU=USB,DC=ms,DC=uhbs,DC=ch"
userpw = "********"
# Domain infos
baseDN = "ou=USB,dc=ms,dc=uhbs,dc=ch"
host = "ms.uhbs.ch"
ldap_url = "ldap://ms.uhbs.ch:389"	

