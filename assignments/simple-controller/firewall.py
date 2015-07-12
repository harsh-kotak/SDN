'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

''' Add your global variables here ... '''



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):
        ''' Add your logic here ... '''
        data = open(policyFile)
        data.readline()
        while 1:
            line = data.readline()
            if not line:
                break
            #print line
            id, mac_0, mac_1 = line.split(',')
            fm = of.ofp_flow_mod(priority = 1000)
            fm.match.dl_src = EthAddr(mac_0)
            fm.match.dl_dst = EthAddr(mac_1)
            fm.match.dl_src = EthAddr(mac_1)
            fm.match.dl_dst = EthAddr(mac_0)
            event.connection.send(fm)

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
