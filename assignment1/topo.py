from mininet.topo import Topo
from mininet.node import Node
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCIntf
from mininet.node import RemoteController

class Router(Node):
    def config (self, **params):
        super(Router, self).config (**params)

    # Routing einschalten 
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate (self):

    # Routing abschalten
        self.cmd('sysctl net.ipv4.ip_forward=0')

        super(Router, self).terminate()

class CustomTopo(Topo):

  __LINK_BANDWIDTH = 1

  def __init__(self):
      Topo.__init__(self)

  def build(self):

    # Switches 
    sw1 = self.addSwitch('sw1', defaultRoute='via 10.0.0.1', dpid='0000000000000001')

    sw2 = self.addSwitch('sw2', defaultRoute='via 10.0.1.1', dpid='0000000000000002')
    
    # Router
    router = self.addHost('router', ip='10.0.0.1/24', cls=Router)

    # Hosts
    h1 = self.addHost('h1', ip='10.0.0.2/24', defaultRoute='via 10.0.0.1', mac='ba:de:af:fe:00:02')
    
    h2 = self.addHost('h2', ip='10.0.0.3/24', defaultRoute='via 10.0.0.1', mac='ba:de:af:fe:00:03')

    h3 = self.addHost('h3', ip='10.0.1.2/24', defaultRoute='via 10.0.1.1', mac='ba:de:af:fe:00:04')
    
    h4 = self.addHost('h4', ip='10.0.1.3/24', defaultRoute='via 10.0.1.1', mac='ba:de:af:fe:00:05')

    #Switches mit Hosts verbinden
    self.addLink(sw1, h1, 1, 1)
    self.addLink(sw1, h2, 2, 1)
    self.addLink(sw2, h3, 1, 1)
    self.addLink(sw2, h4, 2, 1)

    #Router mit Switches verbinden
    self.addLink (router, sw1, 1, 3, intfName1='router-eth1', params1={'ip':'10.0.0.1/24'})
    self.addLink (router, sw2, 2, 3, intfName1='router-eth2', params1={'ip':'10.0.1.1/24'})
  

def run():
  topo = CustomTopo()
  net = Mininet(topo=topo,
                controller=RemoteController('ofp-c1',
                                            ip='127.0.0.1',
                                            port=6633))
  net.start()
  CLI(net)    
  net.stop()


if __name__ == '__main__':
  run()
