'''
Tom Wallace
CSS 645
Spring 2018
Final project
'''

import numpy as np
import pandas as pd
import math
from random import shuffle

def runSimulation(n_iter):

	# import mechanization data
	sechser = pd.read_csv("sechser-saunders-ISQ-2010.tab", sep = '\t')

	# import neighbors data
	contdird = pd.read_csv("contdird.csv")

	# import mid data
	rivals = pd.read_csv("dyadmid20-1.csv")

	# import cinc data
	nmc = pd.read_csv("NMC_5_0.csv")

	# get players for starting year (1979)
	with open("players1979") as f:
		agents1979 = f.readlines()
	agents1979 = [x.replace('"', '') for x in agents1979]
	agents1979 = [x.strip() for x in agents1979]

	# create agents
	lst = []
	for name in agents1979:
		agent = Agent(name)
		lst.append(agent)

	# coeffs
	coeff_enemy_mu = 0.209
	coeff_enemy_ss = 0.081

	coeff_enemy_mech_mu = 0.044
	coeff_enemy_mech_ss = 0.019

	coeff_neighbor_mu = 0.149
	coeff_neighbor_ss = 0.059

	coeff_neighbor_mech_mu = 0.023
	coeff_neighbor_mech_ss = 0.013

	coeff_aml_mu = -0.095
	coeff_aml_ss = 0.044

	for i in range(0, n_iter):

		# get coeffs, starting mech
		for agent in lst:
			agent.drawNeighborSensitivity(coeff_neighbor_mu, coeff_neighbor_ss)
			agent.drawNeighborMechSensitivity(coeff_neighbor_mech_mu,coeff_neighbor_mech_ss)

			agent.drawEnemySensitivity(coeff_enemy_mu, coeff_enemy_ss)
			agent.drawEnemyMechSensitivity(coeff_enemy_mech_mu, coeff_enemy_mech_ss)

			agent.drawAMLSensitivity(coeff_aml_mu, coeff_aml_ss)

			agent.getStartingMech(1979, sechser)

		# steps
		years = [1979, 1981, 1983, 1985, 1987, 
			1989, 1991, 1993, 1995, 
			1997, 1999, 2001]

		for year in years:

			# shuffle in place to ensure random activation order
			shuffle(lst)

			for agent in lst:

				# update perception
				agent.getEnemies(year, rivals)
				agent.getAML(year, sechser)
			
				# update enemy mech
				if(len(agent.enemies) > 0):
					agent.calcEnemyMech(lst)
					agent.calcLogEnemyMech()

				# update neighbor mech
				if(len(agent.neighbors) > 0):
					agent.calcNeighborMech(lst)
					agent.calcLogNeighborMech()

				# update own mech
				agent.updateOwnMech()

				# output
				print(year, agent.name, len(agent.enemies))

class Agent:
	def __init__(self, name):
		self.name = name

		self.mech = 0
		self.log_mech = 0

		self.neighbors = []
		self.neighbor_sensitivity = 0

		self.neighbor_mech = 0
		self.log_neighbor_mech = 0
		self.neighbor_mech_sensitivity = 0

		self.enemies = []
		self.enemy_sensitivity = 0

		self.enemy_mech = 0
		self.enemy_log_mech = 0
		self.enemy_mech_sensitivity = 0

		self.aml = 0
		self.aml_sensitivity = 0

	def drawNeighborSensitivity(self, mu, ss):
		self.neighbor_sensitivity = np.random.normal(mu, ss)

	def drawNeighborMechSensitivity(self, mu, ss):
		self.neighbor_mech_sensitivity = np.random.normal(mu, ss)

	def drawEnemySensitivity(self, mu, ss):
		self.enemy_sensitivity = np.random.normal(mu, ss)

	def drawEnemyMechSensitivity(self, mu, ss):
		self.enemy_mech_sensitivity = np.random.normal(mu, ss)

	def drawAMLSensitivity(self, mu, ss):
		self.aml_sensitivity = np.random.normal(mu, ss)

	def getNeighbors(self, year, df):
		df = df[(df["year"] == year) & (df["state1ab"] == self.name)]
		neighbors = df["state2ab"].tolist()
		self.neighbors = neighbors

	def getEnemies(self, year, df):
		enemiesA = df[(df["NAMEA"] == self.name) & (df["YEAR"] >= year) & (df["YEAR"] <= year)]["NAMEB"].unique().tolist()
		enemiesB = df[(df["NAMEB"] == self.name) & (df["YEAR"] >= year) & (df["YEAR"] <= year)]["NAMEA"].unique().tolist()
		self.enemies = enemiesA + enemiesB

	def getAML(self, year, df):
		aml = df[(df["cabb"] == self.name) & (df["year"] == year)]["antimech_lesson_2"].tolist()[0]
		self.aml = aml

	def getStartingMech(self, year, df):
		log_mech = df[(df["year"] == year) & (df["cabb"] == self.name)]["log_mech"].tolist()[0]
		mech = math.exp(log_mech)
		self.mech = mech

	def calcEnemyMech(self, lst):
		enemies = [x for x in lst if (x.name in self.enemies)]
		mech_enemies = [x for x in enemies if not math.isnan(x.mech)]
		n_mech_enemies = len(mech_enemies)
		enemy_mech = 0
		if(n_mech_enemies > 0):
			for enemy in mech_enemies:
				enemy_mech = enemy_mech + enemy.mech
			self.enemy_mech = enemy_mech / n_mech_enemies
		else:
			self.enemy_mech = 0

	def calcLogEnemyMech(self):
		self.log_enemy_mech = np.log(self.enemy_mech)

	def calcNeighborMech(self, lst):
		neighbors = [x for x in lst if (x.name in self.neighbors)]
		mech_neighbors = [x for x in neighbors if not math.isnan(x.mech)]
		n_mech_neighbors = len(mech_neighbors)
		neighbor_mech = 0
		if(n_mech_neighbors > 0):
			for neighbor in mech_neighbors:
				neighbor_mech = neighbor_mech + neighbor.mech
			self.neighbor_mech = neighbor_mech / n_mech_neighbors
		else:
			self.neighbor_mech = 0
	
	def calcLogEnemyMech(self):
		self.log_neighbor_mech = np.log(self.neighbor_mech)
	
	def calcLogMech(self):
		self.log_mech = np.log(self.mech)

	def updateOwnMech(self):

		if(len(self.enemies) > 0):
			enemy_update = self.enemy_sensitivity * self.mech
			enemy_mech_update = self.enemy_mech_sensitivity * self.enemy_mech
		else:
			enemy_update = 0
			enemy_mech_update = 0

		neighbor_update = self.neighbor_sensitivity * self.mech
		neighbor_mech_update = self.neighbor_mech_sensitivity * self.neighbor_mech

		aml_update = self.aml_sensitivity * self.mech

		self.mech = self.mech + enemy_update + enemy_mech_update + neighbor_update + neighbor_mech_update + aml_update
		

runSimulation(1)
