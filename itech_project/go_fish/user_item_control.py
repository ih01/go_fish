#import data needed from other models
import os
from itech_project import settings
from django.core.management import setup_environ
setup_environ(settings)
from models import UserProfile, Rod, Boat, Bait


#gets the user profile
def get_userProfile(user):
	return UserProfile.objects.get(user=user)
	
#check for user profile
def check_user(request):
	user_prof = None
	try:
		us = request.user
		user_prof = get_userProfile(us)
	except:
		user_prof = None
	context_dict = {}
	context_dict ['user_profile']=user_prof
	return context_dict



#gets the modifier for the users boat
def get_boatMod(user):
	
	#get user profile info
	user_prof = get_userProfile(user)
	#return the modifier
	return user_prof.boat.timeMod

#gets modifier for users rod
def get_rodMod(user):

	#get user profile info
	user_prof = get_userProfile(user)
	#return the modifier
	return user_prof.rod.fishMod


#gets modifier for users bait
def get_baitMod(user):

	#get user profile info
	user_prof = get_userProfile(user)
	#return the modifier
	return user_prof.bait.fishMod


#gets level of users rod
def get_rodLevel(user):
	
	user_prof = get_userProfile(user)
	#return the rods level
	return user_prof.rod.level


#gets level of users boat
def get_boatLevel(user):

	user_prof = get_userProfile(user)
	#return the boats level
	return user_prof.boat.level


#gets level of users bait
def get_baitLevel(user):

	user_prof = get_userProfile(user)
	#return bait level
	return user_prof.bait.level



#gets list of rods available to a user
def get_rodList(user):
	return Rod.objects.filter(level__gt=get_rodLevel(user))


#gets list of boats available to user
def get_boatList(user):
	return Boat.objects.filter(level__gt=get_boatLevel(user))

#gets list of bait available to user
def get_baitList(user):
	return Bait.objects.filter(level__gt=get_baitLevel(user))


#get a rod from db
def getRod(level):
	return Rod.objects.get(pk=int(level))

#get a boat from db
def getBoat(level):
	return Boat.objects.get(pk=int(level))

#get bait from db
def getBait(level):
	return Bait.objects.get(pk=int(level))

#gets users balance status
def get_balance_status(user):
    user_prof = get_userProfile(user)
    return user_prof.balance_status



