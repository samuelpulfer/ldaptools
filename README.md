# ldaptools
Tools for ldap manipulations

## Configuration
Create 2 files in etc/:
  - hostname.py (where hostname is the hostname of the computer you are running the script on)
  - hostname.pass

The Password file will contain the password and nothin else. Whitespace is stripped, so ending newliens are ok.

the config file would look like this:

    # -*- coding: utf-8 -*-
    #
    
    # log files
    modification_logfile="var/modification.log"
    
    # groups to sync
    sync = [
    	{
    		"from": "CN=SrcGroup,DC=Users,DC=example,DC=com", 
    		"to": "CN=TgtGroup,DC=Users,DC=example,DC=com"
    	}, /* etc */
    ]
    
    userdn = "CN=Admin,DC=Users,DC=example,DC=com"
    userpw = None
    
    # Domain infos
    baseDN = "DC=example,DC=com"
    ldap_url = "ldap://dir.example.com:389"	


