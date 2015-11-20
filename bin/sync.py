#!/usr/bin/env python
# -*- coding: utf8 -*-

# setup paths
import os, sys, socket
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'etc'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))

# import modules
import ldaptools
import dirtools
import logging
from logging.handlers import TimedRotatingFileHandler

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

def get_logger(logfile, service_name, level):
	# Logger initialisieren
	l = logging.getLogger(service_name)
	l.setLevel(level)
	#fh = logging.FileHandler(logfile)
	fh = TimedRotatingFileHandler(logfile, 'midnight') # logrotation, 1 file per day
	fh.setLevel(level)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	l.addHandler(fh)
	l.info('==> Starting ' + service_name)
	
	return l

if __name__ == "__main__":
	"""
	LOG LEVELS:
		CRITICAL	50
		ERROR	40
		WARNING	30
		INFO	20
		DEBUG	10
		NOTSET	0
	"""
	log_level = logging.DEBUG
	
	# read configuration and password files from etc. the config file fo this host
	# is looked up under ../etc/`hostname`.py, the pw file under 
	# ../etc/`hostname`.pass
	config = read_config()
	
	# set up logging 
	log_file = config["modification_logfile"]
	if config["modification_logfile"][0] != "/":
		log_file = os.path.dirname(__file__) + "/../" + config["modification_logfile"]
	log = get_logger(log_file, "ldap_sync", log_level)
	
	log.info("Connecting to %s" % (config["ldap_url"]))
	log.info("BindDN %s" % (config["userdn"]))
	
	# connect to ldap server
	try:
		l = dirtools.connect(config["ldap_url"], config["userdn"], config["userpw"])
	except:
		log.critical("Failed to connect")
		sys.exit(2)
	
	# loop over all items which have to be synced
	for entry in config["sync"]:
		log.info("Syncing %s" % entry["from"])
		
		# do a subtree search with our filter from the configuration
		res = dirtools.search(entry["from"], config["baseDN"], True)
		
		# LDAP results contain entries with empty DNs, at least this is what 
		# Microsoft's AD returns. These empty entries are ldap urls pointing to 
		# other directory trees. This is obsolete as of LDAPv3, so we ignore them.
		num_records = dirtools.len(res)
		log.debug("Number of entries found by search: %d" % num_records)
		
		# find all members of all DNs
		cnlist = []
		for r in res:
			if r[0] == None: # skip ldap referers
				continue
			try:
				cnlist = cnlist + r[1]["member"]
			except:
				log.warn("%s does not have a member attribute" % r[0])
		
		log.info("Found %d members in src DNs" % len(cnlist))
		
		# decide which method to use: copy, sync or delete
		
		# copy, preserve all members in target
		log.info("Wiriting to %s" % entry["to"])
		ret = ldaptools.member_copy(l, cnlist, entry["to"])
		log.info(ret)
		#print ldaptools.get_one(l, entry["to"])
		
		# sync, overwrite everything
		#ldaptools.member_sync(l, cnlist, entry["to"])
		
	log.debug("Disconnecting from %s" % config["ldap_url"])
	dirtools.disconnect()
	
	#a = ldaptools.ldaptools()
	#a.sync(config.syncfromcn, config.synctocn)
	#a.commit()
	#del a
