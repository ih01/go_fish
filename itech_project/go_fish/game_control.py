#functions for controlling
#loading/saving and creation of games
#functions pickle data to
#or unpickle from the DB

#import data needed from other models
import os
from itech_project import settings
from django.core.management import setup_environ
setup_environ(settings)
from models import Game, UserProfile, Rod, Boat, Bait
from game import MakeGame
from user_item_control import *
#imported as pickle just in case someone
#wants to revert to regular pickle later
import cPickle as pickle


#find users game
def find_game(user):
	return Game.objects.get(user=user)


#create a new game for the user
#and store it in the DB
def new_game(user):


	#see if duplicate game check needed here
	#create a new game
	newGame = MakeGame()

	#pickle the object into a string
	picGame = pickle.dumps(newGame)
	
	#Store in the DB
	Game.objects.get_or_create(user=user, pickledgame=picGame)
        return newGame
	


#loads a game from the DB and returns the game object
def load_game(user):
	
	#get the users game
	users_game = find_game(user)

	#unpickle it back to an object and return it
	game = pickle.loads(str(users_game.pickledgame))
	return game
	
	

#stores a users game back to the DB
def save_game(user, game):
	
	#pickle the game
	saveGame = pickle.dumps(game)
	
	#find the correct model object in the DB
	users_game = find_game(user)

	#update it with new game state and save to DB
	users_game.pickledgame = saveGame
	users_game.save()


#resets a users game to a new game
def reset_game(user):
	
	#find the users current game
	currentGame = find_game(user)

	#Make a new game and pickle it
	new_game = MakeGame()
	next_game = pickle.dumps(new_game)

	#replace the old game with the new one
	currentGame.pickledgame = next_game
	currentGame.save()

#Adds fish to money
def fishToMoney(user, game):
	#get user profile info
	user_prof = get_userProfile(user)
	#changes fish into money
	user_prof.balance += game.sell_fish()
	#save changes
	user_prof.save()
	
	
#Helps process the end of the game
def check_end_game(user, game):
	#check if game is over
	#by looking at time left
	if (game.get_time())<1:
		#sell all fish
		fishToMoney(user, game)
	
		#reset game for a new day
		reset_game(user)
		
		return True
	else:
		return False


	
