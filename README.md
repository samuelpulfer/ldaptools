# ldaptools
Tools for ldap manipulations

## Configuration
Create 2 files in `etc/`:
  - `hostname.py` (where hostname is the hostname of the computer you are running the script on)
  - `hostname.pass`

The Password file will contain the password and nothing else. Whitespace is stripped, so ending newliens are ok.

the config file would look like this:

    # -*- coding: utf-8 -*-
    #
    
    # log files
    modification_logfile="var/modification.log"
    
    # sync group from group "filter" -> group "to"
    sync = [
    	{
    		# valid ldap query. members of all returned groups are copied to target
    		"from": "(&(cn=groupName)(objectClass=group))",
    		# destination dn, this object's members will be propulated
    		"to": "CN=TgtGroup,DC=Users,DC=example,DC=com",
    		"method": "sync", # sync|copy|delete
    	}, # etc ...
    ]
    
    # find all VD names for users in group "filter", write vd names into group "to"
    sync_vd = [
    	{
    	  "filter": "(& (cn=my_group) (objectClass=group) )", 
    	  "to": "CN=DC=example,DC=com"
    	}, # etc ...
    ]
    
    userdn = "CN=Admin,DC=Users,DC=example,DC=com"
    userpw = None
    
    # Domain infos
    baseDN = "DC=example,DC=com"
    ldap_url = "ldap://example.com:389"	

## Member synchronization
This is straight forward. The executable `bin/sync.py` looks for all members 
found in `sync[...][N]["from"]` and copies all DNs to 
`sync[...][N]["to"]` where the last config value is a DN to an ldap group.

## VD Sync
The second script finds all members in the groups defined in filter 
(config value `sync_vd`). Using a vCenter inventory export to find the mapping 
between sAMAccountName and the vd hostname (this __export needs to be done 
manually__[1]). All found VD DNs will be written to the target group.

The script must be started with one command line parameter pointing to the 
csv export from VMware:
    ./bin/vm_sync.py var/vd-import/vd_import.csv

1] Exporting the sAMAccountName/hosname mapping go to the VMware Horizon View Administrator, then:
*Catalog -> Desktop Pools -> Choose Pool -> Tab Inventory -> Export* (little document with arrow icon)

