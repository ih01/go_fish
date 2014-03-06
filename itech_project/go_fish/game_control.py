#functions for controlling
#loading/saving and creation of games
#all functions pickle data to
#or unpickle from the DB
# -- not yet tested --

#import data needed from other models
#may not be needed if calling module has
#already done this?
import os
from itech_project import settings
from random import randint
from django.core.management import setup_environ
setup_environ(settings)
from models import Game
from game import MakeGame
#imported as pickle just in case someone
#wants to revert to regular pickle later
import cPickle as pickle

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
	


#loads a game from the DB and returns the game object
def load_game(user):
	
	#get the users game
	users_game = Game.objects.get(user=user)

	#unpickle it back to an object and return it
	game = pickle.loads(str(users_game.pickledgame))
	return game
	
	

#stores a users game back to the DB
def save_game(user, game):
	
	#pickle the game
	saveGame = pickle.dumps(game)
	
	#find the correct model object in the DB
	users_game = Game.objects.get(user=user)

	#update it with new game state and save to DB
	users_game.pickledgame = saveGame
	users_game.save()
	



	
