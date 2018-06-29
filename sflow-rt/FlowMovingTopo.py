#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.node import OVSBridge


class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config( self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    def build(self, **_opts):
        r0 = self.addNode("r0", cls=LinuxRouter, ip="192.168.0.1/24", defaultRoute="via 192.168.0.2")
        r1 = self.addNode("r1", cls=LinuxRouter, ip="192.168.0.2/24", defaultRoute="via 192.168.0.1")

        sr = self.addSwitch("s9", cls=OVSBridge)
        s0, s1, s2, s3 = [self.addSwitch(s) for s in ('s0', 's1', 's2', 's3')]

        self.addLink(sr, r0)
        self.addLink(sr, r1)
        self.addLink(s0, r0, intfName2="r0-eth1",
                     params2={"ip": "10.0.0.1/24"})
        self.addLink(s1, r0, intfName2="r0-eth2",
                     params2={"ip": "10.0.1.1/24"})
        self.addLink(s2, r1, intfName2="r1-eth1",
                     params2={"ip": "10.0.2.1/24"})
        self.addLink(s3, r1, intfName2="r1-eth2",
                     params2={"ip": "10.0.3.1/24"})

        for n in range(0, 4):
            for h in range(0, 3):
                name = "n%dh%d" % (n, h)
                ip = "10.0.%d.%d/24" % (n, h + 2)
                mac = "00:00:00:00:0%d:0%d" % (n + 1, h + 1)
                route = "via 10.0.%d.1" % n
                self.addHost(name, ip=ip, mac=mac, defaultRoute=route)
                self.addLink(name, "s%d" % n)


def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo, autoSetMacs=True, controller=lambda name: RemoteController(name, ip="127.0.0.1"))
    net.start()
    net["r0"].cmd("ifconfig r0-eth1 10.0.0.1/24")
    net["r0"].cmd("ifconfig r0-eth2 10.0.1.1/24")
    net["r1"].cmd("ifconfig r1-eth1 10.0.2.1/24")
    net["r1"].cmd("ifconfig r1-eth2 10.0.3.1/24")
    for h in net.hosts:
        h.cmd("sed -i 's/127.0.1.1/202.120.224.6/g' /etc/resolv.conf")

    #net["n1h0"].cmd("nginx")
    #net["n2h0"].cmd("/home/demo/MTDProxy2/install/bin/client")
    #net["n1h0"].cmd("/home/demo/MTDProxy2/install/bin/server")
    #info(net["n0h0"].cmd("curl -x 10.0.2.2:10000 -U test:123456 http://www.test.com"))
    #info(net["n0h0"].cmd("curl http://www.test.com"))
    CLI(net)
    net.stop()


topos = { 'router': NetworkTopo }

if __name__ == '__main__':
    setLogLevel('info')
    run()
