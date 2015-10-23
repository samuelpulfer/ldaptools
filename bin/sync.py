#!/usr/bin/env python
# -*- coding: utf8 -*-



# setup paths
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'etc'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))

# import modules
import config, ldaptools

if __name__ == "__main__":
	a = ldaptools.ldaptools()
	a.sync(config.syncfromcn, config.synctocn)
	a.commit()
	del a
