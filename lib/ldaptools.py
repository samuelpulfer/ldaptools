#!/usr/bin/env python
# -*- coding: utf8 -*-

# setup paths
import os, sys
import ldap
import ldap.modlist as modlist
import logging

## global variables ############################################################

def member_delete(ldapconn, target_group):
	""" delete all "member" attributes of a node
	
	    it expects the following parameters
	    - ldapconn: an ldap connection object
	    - target_group: DN of the target
	"""
	pass

def member_copy(ldapconn, cnlist, target_group):
	""" this methods copies members from one group to another. 
	    
	    member in the target group which are not in the src group will be removed.
	    
	    it expects the following parameters
	    - ldapconn: an ldap connection object
	    - cnlist: list of DNs of new members
	    - target_group: DN of the target
	    
	    Both objects (src, tgt) must be able to have one to many "member" attributes.
	"""
	
	# get target group
	r = get_one(ldapconn, target_group)
	
	# extract existing members
	res = r[0][1]
	if "member" not in res:
		tgt_list = []
	else:
		tgt_list = res["member"]
	
	ret = {
		"method": "copy",
		"old_length": len(tgt_list),
		"new_length": 0,
		"added": 0
	}
	
	#print tgt_list
	
	# append existing members to new members
	new_member = tgt_list[:] # copy rather than reference
	for e in cnlist:
		if e not in new_member:
			new_member.append(e)
			ret["added"] += 1
	
	# create mod list
	mlist = modlist.modifyModlist({'member':tgt_list}, {'member':new_member})
	
	# commit if the modlist is not empty
	ret["new_length"] = ret["old_length"]
	if len(mlist) > 0:
		#print mlist
		if mlist[0][0] == 1:
			ret["new_length"] = len(mlist[1][2])
		else:
			ret["new_length"] = len(mlist[0][2])
			
		ldapconn.modify_s(target_group, mlist)
	
	return ret
	
def member_sync(ldapconn, cnlist, target_group):
	""" this methods syncs members from one group to another. 
	    
	    member in the target group which are not in the src group will remain in the target grp.
	    
	    it expects the following parameters
	    - ldapconn: an ldap connection object
	    - cnlist: list of DNs of new members
	    - target_group: DN of the target
	    
	    Both objects (src, tgt) must be able to have one to many "member" attributes.
	"""
	
	# get target group
	r = get_one(ldapconn, target_group)
	
	# extract existing members
	res = r[0][1]
	if "member" not in res:
		tgt_list = []
	else:
		tgt_list = res["member"]
	
	ret = {
		"method": "sync",
		"old_length": len(tgt_list),
		"new_length": len(cnlist)
	}
	
	# create mod list
	mlist = modlist.modifyModlist({'member':tgt_list}, {'member':cnlist})
	
	# commit if the modlist is not empty
	ret["new_length"] = ret["old_length"]
	if len(mlist) > 0:
		#print mlist
		if mlist[0][0] == 1:
			ret["new_length"] = len(mlist[1][2])
		else:
			ret["new_length"] = len(mlist[0][2])
		
		ldapconn.modify_s(target_group, mlist)
	
	return ret

def get_one(ldapconn, dn):
	parts = dn.split(",")
	cn = parts[0]
	search = ",".join(parts[1:])

	return ldapconn.search_s(search, ldap.SCOPE_ONELEVEL, cn)

'''
class ldaptools(object):
	def __init__(self):
		# Konstruktor
		self.__dntocommit = ""
		self.__ldiftocommit = ""
		# Logger initialisieren
		self.__logger = logging.getLogger('modification')
		self.__logger.setLevel(logging.INFO)
		fh = logging.FileHandler(os.path.join(os.path.dirname(__file__), '..',config.modification_logfile))
		fh.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		fh.setFormatter(formatter)
		self.__logger.addHandler(fh)
		self.__logger.debug('Initialisation abgeschlossen.')
		
	def __del__(self):
		# Logger beenden
		self.__logger.debug('Logger beendet.')
		logging.shutdown()
	# Suche
	"""
		-Verbindung aufbauen
		-Subtree suche ab baseDN
		-gibt List mit allen Ergebnissen zurueck.

	"""
	def search(self, target):
		try:
			l = ldap.open(host)
			l.protocol_version = ldap.VERSION3
			l.simple_bind_s(userdn, userpw)
			self.__logger.debug('Bind hergestellt.')
		except:
			self.__logger.critical('Bind konnte nicht hergestellt werden.')
			return False
		#suche nach testgroup
		self.__logger.debug('Suche nach: ' + target)
		try:
			resultid = l.search(baseDN, ldap.SCOPE_SUBTREE, target, None)
		except:
			self.__logger.critical(sys.exc_info()[0])
			return False
			
		result_set = []
		while 1:
			result_type, result_data = l.result(resultid, 0)
			if result_data == []:
				break
			else:
				if result_type == ldap.RES_SEARCH_ENTRY:
					result_set.append(result_data)
		l.unbind_s()
		self.__logger.debug('Resultat:\n' + str(result_set))
		return result_set
	
	
	# Benutzer einer Gruppe hinzufuegen
	"""
		-Verbindung aufbauen
		-Gruppe suchen
		-Benutzer suchen
		-gibt "ldif" und DN zuruek um Benutzer der Gruppe Hinzuzufuegen.
	
	"""
	def adduser(self, user, group):
		# Benutzer suchen
		userinfos = self.search('CN='+user)
		groupinfos = self.search('CN='+group)
		#TODO hier muss ueberprueft werden ob auch nur ein Benutzer und nur eine Gruppe gefunden wurden.
	
		#Gruppen member suchen
		self.__dntocommit = groupinfos[0][0][0]
		if 'member' in groupinfos[0][0][1]:
			groupmember = groupinfos[0][0][1]['member']
		else:
			groupmember = []
	
		userdn = userinfos[0][0][0]
		#return groupmember, userdn
		#"ldif" generieren
		newgroupmember = groupmember[:]
		newgroupmember.append(userdn)
		self.__ldiftocommit = modlist.modifyModlist({'member':groupmember}, {'member':newgroupmember})
		return self.__ldiftocommit, self.__dntocommit
	
	
	# ldif fuer Gruppensync erstellen	
	"""
		-Verbindung aufbauen
		-Benutzer in Sourcegruppe suchen
		-Benutzer in Targetgruppe suchen
		-gibt "ldif" und DN zuruek um Benutzer aus Sourcegruppe der Targetgruppe Hinzuzufuegen.
	
	"""
	def sync(self, source, target):
		self.__logger.info('Gruppe: ' + source + ' soll nach Gruppe: ' + target + ' synchronisiert werden.')
		groupinfossource = self.search('CN='+source)
		groupinfostarget = self.search('CN='+target)
		groupdnsource = groupinfossource[0][0][0]
		groupdntarget = groupinfostarget[0][0][0]
		self.__logger.info('DN der Quellgruppe: ' + groupdnsource)
		self.__logger.info('DN der Zielgruppe: ' + groupdntarget)
		if 'member' in groupinfossource[0][0][1]:
			groupmembersource = groupinfossource[0][0][1]['member']
		else:
			groupmembersource = []
		if 'member' in groupinfostarget[0][0][1]:
			groupmembertarget = groupinfostarget[0][0][1]['member']
		else:
			groupmembertarget = []
		self.__logger.info('Member in Quellgruppe:\n' + str(groupmembersource))
		self.__logger.info('Member in Zielgruppe:\n' + str(groupmembertarget))
		newgroupmembertarget = groupmembersource[:]
		self.__ldiftocommit = modlist.modifyModlist({'member':groupmembertarget}, {'member':newgroupmembertarget})
		self.__dntocommit = groupdntarget
		return self.__ldiftocommit, self.__dntocommit
	
	
	# ldif auf dn anwenden.
	"""
		-Verbindung aufbauen
		-"ldif" auf dn anwenden
	"""
	def modify(self, ldif, moddn):
		try:
			l = ldap.initialize(ldap_url)
			l.simple_bind_s(userdn, userpw)
			self.__logger.debug('Bind hergestellt')
		except:
			self.__logger.critical('Bind konnte nicht hergestellt werden.')
			return False
		self.__logger.info('folgendes ldif wird auf DN: ' + str(moddn) + ' angewandt:\n' + str(ldif))
		l.modify_s(moddn,ldif)
		l.unbind()
		self.__logger.info('ldif wurde erfolgreich angewandt.')
	
	
	def commit(self):
		if (self.__ldiftocommit and self.__dntocommit):
			self.modify(self.__ldiftocommit, self.__dntocommit)
			return True
		else:
			return False
'''
