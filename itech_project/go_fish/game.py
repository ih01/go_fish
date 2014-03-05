#game logic lives and operates here **un-finished, dont try to use yet**
#basic version 1, just gives random number of fish
#game board state not stored

#import data needed from other models
from random import randint
from models import UserProfile, Rod, Boat, Bait

#Create and store a new game
#with default values of 0, standard equipment
#starting pos 0,0

class CurrentGame(object):
	#defining new game
	def __init__(self,
		TIME_LEFT = 480,
		POSX = 0,
		POSY = 0
		TOTAL_FISH = 0)
	

#constants are:
#basic fish time FISH_TIME
#basic per square move time BASIC_MOVE

#Instancees
#TIME_LEFT 
#POSX  x co-ordinate
#POSY = y co-ordinate
#TOTAL_FISH



	#function for calculating movement and decreasing time
	#location will come in as a parameter
	#BOAT_MULT comes from boat class, via the user profile
	#need to make sure correct data types being used

	def move(newX, newY)
		DISTANCE = abs(newX - POSX)
		DISTANCE += abs(newY - POSY)

		used_boat = Boat.objects.get(Boat.name__exact=User.boat)
	
		MOVE_TIME = DISTANCE*BASIC_MOVE*(used_boat.timeMod)
	
		# check enough time left(not sure if need this yet)
		if MOVE_TIME>TIME_LEFT:
			#do something to say unable to move
		else:
			TIME_LEFT -= MOVE_TIME
			POSX = newX
			POSY = newY
			#data updated, pickle here?

	
	
	#function for fishing
	#for now just dish out random number
	#fish generation being handled seperately

	def fish()
		TIME_LEFT -= FISH_TIME
		return (randint(1, 20))*ROD_MULT*BAIT_MULT


	
