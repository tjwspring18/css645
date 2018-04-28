'''
Tom Wallace
CSS 645
Spring 2018
Final project
'''

import numpy as np
import pandas as pd
import math

def runSimulation():

	coeff_enemies = 1.2
	coeff_neighbors = 1.15
	coeff_aml = 0.9
	coeff_em = 1.04 #differs from their actual coefficient
	coeff_nm = 1.02 #differs from their actual coefficient
	coeff_mountains = 1.1

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

	# get neighbors, enemies, aml, starting mech
	for agent in lst:
		agent.getNeighbors(1979, contdird)
		agent.getEnemies(1979, rivals)
		agent.getAML(1979, sechser)
		agent.getStartingMech(1979, sechser)

	# calculate enemy_mech and neighbor_mech
	for agent in lst:
		if(len(agent.enemies) > 0):
			agent.calcEnemyMech(lst)
			agent.calcNeighborMech(lst)
	
	# 1981
	'''
	for agent in lst:
		print(agent.name, agent.current_mech, agent.mech, agent.neighbors, agent.neighbor_mech, agent.enemies,
				agent.enemy_mech, agent.aml)
	'''

class Agent:
	def __init__(self, name):
		self.current_mech = 0
		self.mech = 0
		self.name = name
		self.neighbors = []
		self.neighbor_mech = 0
		self.enemies = []
		self.enemy_mech = 0
		self.aml = 0

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
		self.current_mech = mech

	def calcEnemyMech(self, lst):
		enemies = [x for x in lst if (x.name in self.enemies)]
		mech_enemies = [x for x in enemies if not math.isnan(x.current_mech)]
		n_mech_enemies = len(mech_enemies)
		enemy_mech = 0
		if(n_mech_enemies > 0):
			for enemy in mech_enemies:
				enemy_mech = enemy_mech + enemy.current_mech
			self.enemy_mech = enemy_mech / n_mech_enemies
		else:
			self.enemy_mech = 0

	def calcNeighborMech(self, lst):
		neighbors = [x for x in lst if (x.name in self.neighbors)]
		mech_neighbors = [x for x in neighbors if not math.isnan(x.current_mech)]
		n_mech_neighbors = len(mech_neighbors)
		neighbor_mech = 0
		if(n_mech_neighbors > 0):
			for neighbor in mech_neighbors:
				neighbor_mech = neighbor_mech + neighbor.current_mech
			self.neighbor_mech = neighbor_mech / n_mech_neighbors
		else:
			self.neighbor_mech = 0

runSimulation()
