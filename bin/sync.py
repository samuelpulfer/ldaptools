#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Synchronize directory groups

This script copies all members of a list of groups to another group. Members
may be replaced or added.

If a member of a target group is objectClass=group, it will not be purged.

(c) 2015, Simon Wunderlin
"""

# setup paths
import os, sys, socket
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'etc'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))

# import modules
import dirtools
import dirsync
import logging
from logging.handlers import TimedRotatingFileHandler

def read_config():
	""" this method looks for a config file in etc/`hostname`.py. The file 
	    is treated like a regular python file (__import__) and if successfuly 
	    imported the file's attributes will be returned as a dict.
	"""
	
	# configuration 
	config = {}
	
	# resolve path to current file
	basepath = os.path.dirname(os.path.realpath(__file__)) + "/"
	
	# get hostname
	hostname = socket.gethostname()
	
	# path to config file directory
	configpath = os.path.realpath(basepath+'../etc')
	
	# file containing configuration for this host
	configfile = os.path.realpath(configpath+'/%s.py' % hostname)
	
	# file containing pasword for this host (whitespace stripped)
	passfile = os.path.realpath(configpath+'/%s.pass' % hostname)
	
	# add config directory to include paths
	sys.path.append(configpath)
	try:
		# include config file
		cfgfile = __import__(hostname)
	except:
		# most probably the file doe not exist or is not readable
		e = sys.exc_info()[0]
		msg = "Failed to read config file '%s', make sure it exists." % (configfile)
		sys.stderr.write(msg+"\n")
		sys.stderr.write(str(e))
		sys.exit(2)
	
	# copy all attributes for configfile to config
	attrs = [a for a in dir(cfgfile) if not a.startswith('__')]
	for a in attrs:
		config[a] = getattr(cfgfile, a)
	
	# read password from file
	try:
		with open(passfile) as f: 
			config["userpw"] = f.read()
			config["userpw"] = config["userpw"].strip() # remove trailing whitespace
	except:
		# most probably the file doe not exist or is not readable
		e = sys.exc_info()[0]
		print("Error while loading password file %s") % passfile
		sys.stderr.write(str(e))
		sys.exit(3)
		
	return config

def get_logger(logfile, service_name, level):
	# Logger initialisieren
	l = logging.getLogger(service_name)
	l.setLevel(level)
	
	# log rotation every day
	fh = TimedRotatingFileHandler(logfile, 'midnight') # logrotation, 1 file per day
	fh.setLevel(level)
	
	# standard unix log file format
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	l.addHandler(fh)
	
	# log startup
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
		log.info("Wiriting to %s" % entry["to"])
		
		#from pprint import pprint
		#pprint(entry)
		
		if entry["method"] == "sync":
			# copy all members from src to target, deleting everything not in src
			ret = dirsync.member_sync(l, cnlist, entry["to"])
		elif entry["method"] == "copy":
			# copy all from src to tgt, preserving existing members in tgt
			ret = dirsync.member_copy(l, cnlist, entry["to"])
		elif entry["method"] == "delete":
			# delete all members
			raise ValueError('Method delete not implemented')
		else:
			raise ValueError('Unknown method: %s' % entry["method"])
		
		log.info("result: " + str(ret))
		
	# all done, close connection to ldap server
	log.debug("Disconnecting from %s" % config["ldap_url"])
	dirtools.disconnect()

