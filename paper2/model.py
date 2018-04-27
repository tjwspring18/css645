def runSimulation():

	years = [1979, 1981, 1983, 1985, 1987, 1989, 1991, 1993, 1995, 1997,
			1999, 2001]

	# get players for starting year (1979)
	with open("players1979") as f:
		agents1979 = f.readlines()
	agents1979 = [x.strip() for x in agents1979]

	# create agents
	lst1979 = []
	for name in agents1979:
		agent = Agent(name)
		lst1979.append(agent)

	# read neighbors data
	for agent in lst1979:
		agent.addNeighbor("foo")
		agent.addNeighbor("bar")
		print(agent.neighbors)
	
class Agent:
	def __init__(self, name):
		self.name = name
		self.log_mech = 0
		self.neighbors = []
		self.enemies = []

	def addNeighbor(self, name):
		self.neighbors.append(name)
	

'''
lst = []
for country in countries:
	agent = State(country)
	lst.append(agent)
	'''
runSimulation()
