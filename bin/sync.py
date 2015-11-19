#!/usr/bin/env python
# -*- coding: utf8 -*-

# setup paths
import os, sys, socket
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'etc'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))

# import modules
import ldaptools
import dir as dirtools

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
		print("Error while loading password file %s") % passfile
		sys.exit(3)
		
	return config

if __name__ == "__main__":
	config = read_config()
	
	#print config
	
	l = dirtools.connect(config["ldap_url"], config["userdn"], config["userpw"])
	print l
	dirtools.disconnect()
	
	#a = ldaptools.ldaptools()
	#a.sync(config.syncfromcn, config.synctocn)
	#a.commit()
	#del a
