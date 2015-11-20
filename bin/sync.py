#!/usr/bin/env python
# -*- coding: utf8 -*-

# setup paths
import os, sys, socket
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'etc'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))

# import modules
import ldaptools
import dirtools

def read_config():
	""" this method looks for a config file in etc/`hostname`.py. The file 
	    is treated like a regular python file (__import__) and if successfuly 
	    imported the file's attributes will be returned as a dict."""
	config = {}
	basepath = os.path.dirname(os.path.realpath(__file__)) + "/"
	hostname = socket.gethostname()
	configpath = os.path.realpath(basepath+'../etc')
	configfile = os.path.realpath(configpath+'/%s.py' % hostname)
	passfile = os.path.realpath(configpath+'/%s.pass' % hostname)
	
	sys.path.append(configpath)
	try:
		cfgfile = __import__(hostname)
	except:
		e = sys.exc_info()[0]
		msg = "Failed to read config file '%s', make sure it exists." % (configfile)
		sys.stderr.write(msg+"\n")
		sys.stderr.write(str(e))
		sys.exit(2)
	
	attrs = [a for a in dir(cfgfile) if not a.startswith('__')]
	for a in attrs:
		v = getattr(cfgfile, a)
		#print "%s=%s" % (a, v)
		config[a] = v
	
	try:
		with open(passfile) as f: 
			config["userpw"] = f.read()
			config["userpw"] = config["userpw"].strip() # remove trailing whitespace
	except:
		e = sys.exc_info()[0]
		print("Error while loading password file %s") % passfile
		sys.stderr.write(str(e))
		sys.exit(3)
		
	return config

if __name__ == "__main__":
	
	# read configuration and password files from etc. the config file fo this host
	# is looked up under ../etc/`hostname`.py, the pw file under 
	# ../etc/`hostname`.pass
	config = read_config()
	
	# connect to ldap server
	l = dirtools.connect(config["ldap_url"], config["userdn"], config["userpw"])
	
	# loop over all items which have to be synced
	for entry in config["sync"]:
		# debug
		#print entry["from"]
		#print entry["to"]
		
		# do a subtree search with our filter from the configuration
		res = dirtools.search(entry["from"], config["baseDN"], True)
		
		# LDAP results contain entries with empty DNs, at least this is what 
		# Microsoft's AD returns. These empty entries are ldap urls pointing to 
		# other directory trees. This is obsolete as of LDAPv3, so we ignore them.
		num_records = dirtools.len(res)
		print num_records
		
		# debug
		#dirtools.listdn(res)
	
	
	dirtools.disconnect()
	
	#a = ldaptools.ldaptools()
	#a.sync(config.syncfromcn, config.synctocn)
	#a.commit()
	#del a
