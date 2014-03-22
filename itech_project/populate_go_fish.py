import os
from itech_project import settings
from django.core.management import setup_environ
setup_environ(settings)
from go_fish.models import Bait, Rod, Boat, UserProfile, Game
from django.contrib.auth.models import User
from go_fish.game_control import *

def populate():
   
# Add item data here

	# Rods
	rod1=add_rod(name="Wooden Fishing Rod",
    level = "1",
	cost="0",
	fishMod="1",
    modDescriptor = "1")
	
	rod2=add_rod(name="Iron Fishing Rod",
	level = "2",
	cost="100",
	fishMod="2",
    modDescriptor = "2")
	
	rod3=add_rod(name="Steel Fishing Rod",
	level = "3",
	cost="500",
	fishMod="4",
    modDescriptor = "4")

	rod4=add_rod(name="Mithril Fishing Rod",
	level = "4",
	cost="1000",
	fishMod="8",
    modDescriptor = "8")
	
	# Boats	
	boat1=add_boat(name="Raft",
	level = "1",
	cost="0",
	timeMod="1",
    modDescriptor = "0")
	
	boat2=add_boat(name="Kayak",
	level = "2",
	cost="100",
	timeMod="0.75",
    modDescriptor = "25")

	boat3=add_boat(name="Motor boat",
	level = "3",
	cost="500",
	timeMod="0.5",
    modDescriptor = "50")
	
	boat4=add_boat(name="Speed boat",
	level = "4",
	cost="1000",
	timeMod="0.25",
    modDescriptor = "75")

	# Baits	
	bait1=add_bait(name="Worm",
	level = "1",
	cost="0",
	fishMod="1",
    modDescriptor = "1")
	
	bait2=add_bait(name="Basic Lure",
	level = "2",
	cost="60",
	fishMod="2",
    modDescriptor = "2")

	bait3=add_bait(name="Advanced Lure",
	level = "3",
	cost="300",
	fishMod="3",
    modDescriptor = "3")
	
	bait4=add_bait(name="Bucket O'Bait",
	level = "4",
	cost="600",
	fishMod="4",
    modDescriptor = "4")

#Sample User Data
	player1=add_player("FischerMann", "test", rod1, boat1, bait1, "6000")
	player2=add_player("SaltySeaDog", "test", rod4, boat4, bait3, "5000")
	
  
def add_rod(name, level, cost, fishMod, modDescriptor):
    r = Rod.objects.get_or_create(name=name, level=level, cost=cost, fishMod=fishMod, modDescriptor=modDescriptor)[0]
    return r

def add_bait(name, level, cost, fishMod, modDescriptor):
    B = Bait.objects.get_or_create(name=name, level=level, cost=cost, fishMod=fishMod, modDescriptor=modDescriptor)[0]
    return B

def add_boat(name, level, cost, timeMod, modDescriptor):
    b = Boat.objects.get_or_create(name=name, level=level, cost=cost, timeMod=timeMod, modDescriptor=modDescriptor)[0]
    return b

def add_game(user, pickledgame):
    g = Game.objects.get_or_create(user=user, pickledgame=pickledgame)[0]
    return g

def add_player(name, pw, rod1, boat1, bait1, balance):

    email = '{0}@{1}.com'.format(name,name)
    try:
        u = User.objects.get(username=name)
    except:
        u = User(username=name, email=email)
        u.set_password(pw)
        u.save()
        up = UserProfile(user=u, balance=balance, rod=rod1, boat=boat1, bait=bait1)
        up.save()
	new_game(u)
    return u

# Start execution here!
if __name__ == '__main__':
    print "Starting go_fish population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech_project.settings')
    populate()

