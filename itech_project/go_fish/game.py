#game state lives here
#processes movement and fishing

#import data needed from other models
#import os
#from itech_project import settings
from yield_gen import yieldGenerator
from django.core.management import setup_environ
setup_environ(settings)

#Create and store a new game
#with default values of 0, standard equipment
#starting pos 0,0
#In-game time given 8 hours (480 minutes)

class MakeGame(object):
	#defining new game
	def __init__(self,
		TIME_REMAINING = 480,
		X_COORD = 0,
		Y_COORD = 0,
		TOTAL_FISH = 0):
		
		self.time_left = TIME_REMAINING
		self.posX = X_COORD
		self.posY = Y_COORD
		self.fishTotal = TOTAL_FISH
		#need to include new yeild generator for each new game
		#here so it is saved when game is stored
		self.generator = yieldGenerator()
		
	#basic time used to fish - FISH_TIME
	#basic per square move time - BASIC_MOVE
	FISH_TIME = 15
	BASIC_MOVE = 60
	

	#function for calculating movement and decreasing time
	#location will come in as a parameter
	#needs to be passed user object
	#timeMod comes from boat class

	def move(self, newX, newY, moveMod):
		#calculate distance moved
		distance = abs(newX - self.posX)
		distance += abs(newY - self.posY)

		#calculate move time
		move_time = distance*self.BASIC_MOVE*moveMod
	
		#update time left
		self.time_left -= move_time
	
		#update position.
		self.posX = newX
		self.posY = newY

	
	
	#function for fishing
	#for now just dish out random number
	#fish generation being handled seperately

	def fish(self, rod_mod, bait_mod):

		#reduce time left by fishing time
		self.time_left -= self.FISH_TIME
		
		#apply multipliers
		fish_caught = self.generator.deplete(self.posX, self.posY, rod_mod, bait_mod)

		#update fish total
		self.fishTotal += fish_caught

		#return the fish caught this round
		return fish_caught
	


	#function to facilitate selling fish
	#returns total number of fish
	#and resets total fish count to zero
	def sell_fish(self):
		
		#keep a note of total
		fishExchanged = self.fishTotal

		#reset game total to zero
		self.fishTotal = 0

		return fishExchanged
	


	#some functions for returning values
	#to aid decoupling

	#Returning time left	
	def get_time(self):
		return self.time_left

	#return x coordinate
	def get_X(self):
		return self.posX

	#return y coordinate
	def get_Y(self):
		return self.posY

	
