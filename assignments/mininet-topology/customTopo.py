'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        # Add your logic here ...
        self.linkopts1 = linkopts1
        self.linkopts2 = linkopts2
        self.linkopts3 = linkopts3
        self.fanout = fanout
        i = 1
        j = 1
        # Create Core Switch
        core = self.addSwitch('s%s' %i)
        i = i+1
        # Create Tree of Switches and Hosts
        for aggreg in range(0, fanout):
            aggre = self.addSwitch('s%s' % i)
            i = i+1
            self.addLink(core, aggre, **linkopts1)

            for edg in range(0, fanout):
                edge = self.addSwitch('s%s' % i)
                i = i+1
                self.addLink(aggre, edge, **linkopts2)

                for hos in range(0, fanout):
                    host = self.addHost('h%s' % j)
                    j = j+1
                    self.addLink(edge, host, **linkopts3)

def simpleTest():
    "Create and test a simple network"
    linkopts1 = {'bw':100, 'delay':'5ms'}
    linkopts2 = {'bw':50, 'delay':'10ms'}
    linkopts3 = {'bw':5, 'delay':'20ms'}
    "linkopts1 = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)"
    topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=2)
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    print "Testing bandwidth between h1 and h4"
    h1, h4 = net.get('h1', 'h4')
    net.iperf((h1, h4))
    net.stop()

if __name__ == '__main__':
   # Tell mininet to print useful information
   setLogLevel('info')
   simpleTest()

topos = { 'custom': ( lambda: CustomTopo() ) }
