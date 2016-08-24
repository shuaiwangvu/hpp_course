# gepetto-viewer-server
# not hpp-manipulation-server
# hppcorbaserver
# -DCMAKE_INSTALL_PREFIX=/home/airobert/HPP/install


from HyQ import HyQ
from Agent import PR2
from Environment import BasicHouse
from Obstacle import Obstacle
from hpp.corbaserver import ProblemSolver
# from hpp.corbaserver.manipulation import ProblemSolver as MProblemSolver, ConstraintGraph
from hpp.gepetto import PathPlayer
from hpp.gepetto import ViewerFactory
# from hpp.gepetto.manipulation import ViewerFactory as MViewerFactory
from hpp.corbaserver.manipulation import robot as METARobot


class Platform ():
	main_agent = None
	meta_agent = None
	agents = []
	# problem solver
	ps = None
	# path player
	pp = None
	# view factory
	vf = None
	# viewer
	r = None
	env = None
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
	# 	self.r = self.vf.createViewer()
		self.r.computeObjectPosition()

		#and finally, set the environment
	def setEnvironment(self, env):
		self.vf.loadObstacleModel(env.packageName, env.urdfName, env.name)
		self.env = env
		self.r = self.vf.createViewer()
		# self.refreshDisplay()

	# this method looks useless so far.....
	def activatePlatform(self):
		self.main_agent.client.problem.selectProblem('0')
		for i in self.agents:
			i.refrechAgent()

	def loadAgentView (self, index):
		self.vf = ViewerFactory (self.agents[index -1].ps)
		self.r = self.vf.createViewer()
		# print '---------------->', len(self.agents[index - 1].init_config)
		self.r(self.agents[index - 1].init_config)
		self.refreshDisplay()
		# self.r.computeObjectPosition()

	def playAllPath(self):
		max_time = 0
		for a in self.agents:
			if len(a.plan_proposed) > a:
				a = len(a.plan_proposed)
		
		for t in range(max_time):
			print 'time is ', t
			for i in range(len(self.agents)):
				if len(self.agents[i].plan_proposed) > t:
					self.loadAgentView(i)
					# and then set the agent to its current configuration
					self.r(self.agents[i].plan_proposed[t])


	def playAgentPath(self, cl):
		self.pp = PathPlayer (cl, self.r)
		self.pp.setSpeed(4) # comment this out if you are not debugging
		self.pp.displayPath(0, color = [0.3, 0.7, 0.6, 1], jointName='base_joint_xy')
		self.pp(0)

	def addAgent(self, agt):
		self.agents.append(agt)