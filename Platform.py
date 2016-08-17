# gepetto-viewer-server
# hppcorbaserver
# -DCMAKE_INSTALL_PREFIX=/home/airobert/HPP/install

from HyQ import HyQ
from PR2 import PR2
from Environment import BasicHouse
from Obstacle import Obstacle
from hpp.corbaserver import ProblemSolver
from hpp.gepetto import ViewerFactory
from hpp.gepetto import PathPlayer

class Platform ():
	main_agent = None
	agents = []
	# problem solver
	ps = None
	# path player
	pp = None
	# view factory
	vf = None
	# viewer
	r = None
	# pp = PathPlayer (rbprmBuilder.client.basic,ls r)
	def __init__(self, mainAgentType):
		print 'creating a platform with an agent of type: ', mainAgentType
		if (mainAgentType == "hyq" or mainAgentType == "HyQ" or mainAgentType == "HYQ"):
			self.main_agent = HyQ(self, 1, "main")
		elif (mainAgentType == "pr2" or mainAgentType == "PR2"):
			self.main_agent = PR2(self, 1, "main")
		else:
			print 'this type of agent can not be defined yet'
		self.ps = ProblemSolver (self.main_agent)
		self.vf = ViewerFactory (self.ps)
		self.r = self.vf.createViewer()
		self.r(self.main_agent.getCurrentConfig ())
		self.agents.append (self.main_agent)
		
	def refreshDisplay(self):
		self.r.computeObjectPosition()
		self.r = self.vf.createViewer()

		#and finally, set the environment
	def setEnvironment(self, env):
		self.vf.loadObstacleModel(env.packageName, env.urdfName, env.name)
		self.refreshDisplay()

	
	def activatePlatform(self):
		self.main_agent.client.problem.selectProblem('0')
		for i in self.agents:
			i.refrechAgent()


	def playAgentPath(self, cl):
		self.pp = PathPlayer (cl, self.r)
		self.pp(0)

	def addAgent(self, agt):
		self.agents.append(agt)