#game state lives here
#processes movement and fishing
#version 1, just gives random number of fish

#import data needed from other models
import os
from itech_project import settings
from random import randint
from django.core.management import setup_environ
setup_environ(settings)
from models import UserProfile, Rod, Boat, Bait

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
		
	#basic time used to fish - FISH_TIME
	#basic per square move time - BASIC_MOVE
	FISH_TIME = 15
	BASIC_MOVE = 60
	

	#function for calculating movement and decreasing time
	#location will come in as a parameter
	#needs to be passed user object
	#timeMod comes from boat class

	def move(self, user, newX, newY):
		#calculate distance moved
		distance = abs(newX - self.posX)
		distance += abs(newY - self.posY)
	
		#access users profile to get current equipment
		user_prof = UserProfile.objects.get(user=user)
			
		#calculate move time
		move_time = distance*self.BASIC_MOVE*(user_prof.boat.timeMod)
	
		#update time left
		self.time_left -= move_time
	
		#update position.
		self.posX = newX
		self.posY = newY

	
	
	#function for fishing
	#for now just dish out random number
	#fish generation being handled seperately

	def fish(self, user):

		#reduce time left by fishing time
		self.time_left -= self.FISH_TIME
		
		#access users profile to get current equipment
		user_prof = UserProfile.objects.get(user=user)
		
		#call to fish generation will go here
		basic_fish = (randint(1, 20))
		
		#apply multipliers
		fish_caught = basic_fish*(user_prof.rod.fishMod)*(user_prof.bait.fishMod)

		#update fish total
		self.fishTotal += fish_caught

		#return the fish caught this round
		return fish_caught
	
	