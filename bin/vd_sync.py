#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
FIXME: this executable should make use of the dirtools library
"""


import os
import ldap, ldif, sys, re
import pprint
#from datetime import datetime
import datetime
import ldap.filter
import csv
import socket
import ldap.modlist as modlist

l = None

config = {
	"uri": None,
	"binddn": None,
	"pass": None,
	"base": "dc=ms,dc=uhbs,dc=ch", # where to look for computers
	"search_filter": "(objectClass=user)",
	"vdlist": None,
	"sync": []
};


def get_ma(filter, dst):
	
	cnlist = []
	
	# find groups of interest
	#f = "(|(cn=MQ_ANA_AA)(cn=MQ_ANA_OA)(cn=MQ_ANA_LA))"
	base = "OU=Exchange_Adressbuecher,OU=PITServer,"+config["base"]
	res = l.search_s(base, ldap.SCOPE_SUBTREE, filter)
	for r in res:
		cnlist = cnlist + r[1]["member"]
	
	#pprint.pprint(cnlist)
	
	result = [] # list of (user, cn, sAMAccountName)
	aduser = [] # list of sAMAccountName
	dnlist = [] # all dn with a sAMAccountName
	for u in cnlist:
		f = re.sub(r'([^\\]),.*', "\\1", u)
		f = f.replace("\\,", ",")
		cn = f
		dn = u
		f = ldap.filter.escape_filter_chars(f, 0);
		
		res = l.search_s("OU=USB,"+config["base"], ldap.SCOPE_SUBTREE, f)
		samaccountname = None
		try:
			#print res[0][1]["sAMAccountName"][0]
			samaccountname = res[0][1]["sAMAccountName"][0]
		except:
			pass
		if samaccountname == None:
			continue
		
		result.append( (u, cn, samaccountname.lower()) )
		aduser.append(samaccountname.lower())
		dnlist.append(dn)
		
	#print cnlist
	#print aduser
	
	vdlist = []
	#read csv file
	with open(config["vdlist"], 'rb') as csvfile:
		hostreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in hostreader:
			adname = ""
			try:
				adname = row[2].split("\\")[1].lower()
				#print adname
			except:
				pass
			
			if adname not in aduser:
				continue
			
			if adname in cfg.sync_vd_ignore_user:
				continue

			# resolve the full dn of the vd
			vddn = None
			try:
				r = l.search_s("OU=USB,"+config["base"], ldap.SCOPE_SUBTREE, "cn="+row[0])
				vddn = r[0][0]
			except:
				pass
			
			ix = aduser.index(adname)
			#print "%s;%s" % (vddn, dnlist[ix])
			vdlist.append(vddn)
		#pp.pprint(vdlist)
		commit(vdlist, dst)
		return len(vdlist)

def commit(members, dn):
	parts = dn.split(",")
	cn = parts[0]
	search = ",".join(parts[1:])

	r = l.search_s(search, ldap.SCOPE_SUBTREE, cn)
	res = r[0][1]
	if "member" not in res:
		srclist = []
	else:
		srclist = res["member"]
	
	mlist = modlist.modifyModlist({'member':srclist}, {'member':members})
	#print dn
	pp.pprint(mlist)
	
	if len(mlist) > 0:
		l.modify_s(dn, mlist)

cfg = None	
def main():
	global l	
	
	l = ldap.initialize(config["uri"])
	l.protocol_version = ldap.VERSION3
	l.simple_bind_s(config["binddn"], config["pass"])
	
	count = 0
	for dst in config["sync"]:
		print "%s" % dst["filter"]
		count += get_ma(dst["filter"], dst["to"])
	
	print "Total count of VDs: %s" % count
	l.unbind_s()

if __name__ == "__main__":
	pp = pprint.PrettyPrinter(indent=4)
	print "=====> %s" % str(datetime.datetime.now())
	
	# argument 1 must contain the path to the import file
	try:
		config["vdlist"] = sys.argv[1]
	except:
		sys.stderr.write("argument 1 must be a path to the import CSV file\n");
		sys.exit(1)
	
	# read password
	basepath = os.path.dirname(os.path.realpath(__file__)) + "/"
	hostname = socket.gethostname()
	passfile = basepath+'../etc/%s.pass' % hostname 
	try:
		with open(passfile) as f: 
			config["pass"] = f.read()
			config["pass"] = config["pass"].strip() # remove trailing whitespace
	except:
		print("Error while loading password file %s") % passfile
		sys.exit(2)
	
	# read config
	def read_cfg():
		sys.path.append(basepath+'../etc/')
		#print basepath+'../etc/'
		try:
			#from shell1 import *
			cfgfile = __import__(hostname)
		except:
			msg = "Make sure the config file '%s' exists." % ('../etc/'+hostname+".py")
			sys.stderr.write(msg+"\n")
			sys.exit(2)
		config["uri"] = cfgfile.ldap_url
		config["binddn"] = cfgfile.userdn
		config["base"] = cfgfile.baseDN
		config["sync"] = cfgfile.sync_vd
		
		global cfg
		cfg = cfgfile
	
	read_cfg()
	
	main()
	
