"""

Author:			Jian Li (jli263@usc.edu)

File Name:		fat.py

Description:	This is a fat tree topology with (k = 4)

"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class FatTopo(Topo):
	"""
	Declare host and switch lists
	"""
	HostList = []
	CoreList = []
	AggrList = []
	EdgeList = []

	def __init__(self, n):
		self.NoOfCore = n
		self.NoOfAggr = n * 2
		self.NoOfEdge = n * 2
		self.NoOfHost = n * 4
		self.NoOfPod = n

		# Initialize topology
		Topo.__init__(self)

		# buildup the topology
		self.buildup()
	
	"""
	Add hosts and switches
	"""
	def addHosts(self):
		for pod in range(0, self.NoOfPod):
			for h in range(1, self.NoOfPod + 1):
				self.HostList.append(self.addHost('3'+str(pod)+str(h)))
	
	def addCoreSwitches(self):
		for i in range(1, self.NoOfCore + 1):
			self.CoreList.append(self.addSwitch('00'+str(i)))
	
	def addAggrSwitches(self):
		for pod in range(0, self.NoOfPod):
			self.AggrList.append(self.addSwitch('1'+str(pod)+'1'))
			self.AggrList.append(self.addSwitch('1'+str(pod)+'2'))
	
	def addEdgeSwitches(self):
		for pod in range(0, self.NoOfPod):
			self.EdgeList.append(self.addSwitch('2'+str(pod)+'1'))
			self.EdgeList.append(self.addSwitch('2'+str(pod)+'2'))
		
	"""
	Add links
	"""
	def	addLinks(self):
		# Add links between Core and Aggregation layers
		for i in range(0, self.NoOfAggr, 2):
			self.addLink(self.CoreList[0], self.AggrList[i])
			self.addLink(self.CoreList[1], self.AggrList[i])
		for i in range(1, self.NoOfAggr, 2):
			self.addLink(self.CoreList[2], self.AggrList[i])
			self.addLink(self.CoreList[3], self.AggrList[i])

		# Add links sbetween Aggregation and Edge layers
		for pod in range(0, self.NoOfPod):
			self.addLink(self.AggrList[pod*2], self.EdgeList[pod*2])
			self.addLink(self.AggrList[pod*2], self.EdgeList[pod*2+1])
			self.addLink(self.AggrList[pod*2+1], self.EdgeList[pod*2])
			self.addLink(self.AggrList[pod*2+1], self.EdgeList[pod*2+1])

		# Add links between Edge layer and Hosts
		for i in range(0, self.NoOfEdge):
			self.addLink(self.EdgeList[i], self.HostList[i*2])
			self.addLink(self.EdgeList[i], self.HostList[i*2+1])

	"""
	Build the topology
	"""
	def buildup(self):
		self.addHosts()
		self.addCoreSwitches()
		self.addAggrSwitches()
		self.addEdgeSwitches()
		self.addLinks()


"""
Simple test
def simpleTest():
	"Create and test a simple network"
	topo = FatTopo(4)
	topo.buildup()
	net = Mininet(topo)
	net.start()
	print "Dumping host connectios"
	dumpNodeConnections(net.hosts)
	print "Testing network connectivity"
	net.pingAll()
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	simpleTest()
"""
topos = { 'fattopo': ( lambda: FatTopo(4) ) }
