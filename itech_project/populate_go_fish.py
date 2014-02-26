import os
from itech_project import settings
from django.core.management import setup_environ
setup_environ(settings)
from go_fish.models import Bait, Rod, Boat, UserProfile, Game
from django.contrib.auth.models import User

def populate():
   
# Add item data here

	# Rods
	add_rod(name="Wooden Fishing Rod",
	cost="0",
	fishMod="2")
	
	add_rod(name="Iron Fishing Rod",
	cost="100",
	fishMod="4")
	
	add_rod(name="Steel Fishing Rod",
	cost="500",
	fishMod="6")

	add_rod(name="Mithril Fishing Rod",
	cost="1000",
	fishMod="8")
	
	# Boats	
	add_boat(name="Raft",
	cost="0",
	timeMod="2")
	
	add_boat(name="Kayak",
	cost="100",
	timeMod="4")

	add_boat(name="Motor boat",
	cost="500",
	timeMod="6")
	
	add_boat(name="Speed boat",
	cost="1000",
	timeMod="8")

	# Baits	
	add_bait(name="Worm",
	cost="0",
	fishMod="1")
	
	add_bait(name="Basic Lure",
	cost="60",
	fishMod="2")

	add_bait(name="Advanced Lure",
	cost="300",
	fishMod="3")
	
	add_bait(name="Bucket O'Bait",
	cost="600",
	fishMod="4")

# Sample User Data

	add_player("Fischer Mann", "Test")
	add_player("Salty Sea Dog", "Test")
	
	# adding user profiles or games doesn't work here, but can be done manually.	
	
	# User Profiles
	# add_profile(user="Fischer Mann",
	# fishAmount="600",
	# rod="Iron Fishing Rod",
	# boat="Raft",
	# bait="Advanced Lure")

	# add_profile(user="Salty Sea Dog",
	# fishAmount="600",
	# rod="Wooden Fishing Rod",
	# boat="Speed boat",
	# bait="Bucket O'Bait")

	# Games
	# add_game(user="Fischer Mann",
	# pickledgame="faszg")

	# add_game(user="Salty Sea Dog",
	# pickledgame="sg\g")
  
def add_rod(name, cost, fishMod):
    r = Rod.objects.get_or_create(name=name, cost=cost, fishMod=fishMod)[0]
    return r

def add_bait(name, cost, fishMod):
    B = Bait.objects.get_or_create(name=name, cost=cost, fishMod=fishMod)[0]
    return B

def add_boat(name, cost, timeMod):
    b = Boat.objects.get_or_create(name=name, cost=cost, timeMod=timeMod)[0]
    return b

def add_game(user, pickledgame):
    g = Game.objects.get_or_create(user=user, pickledgame=pickledgame)[0]
    return g

def add_profile(user, fishAmount, rod, boat, bait):
    p = UserProfile.objects.get_or_create(user=user, fishAmount=fishAmount, rod=rod, boat=boat, bait=bait)[0]
    return p

def add_player(name, pw):

    email = '{0}@{1}.com'.format(name,name)
    try:
        u = User.objects.get(username=name)
    except:
        u = User(username=name, email=email)
        u.set_password(pw)
        u.save()
        up = UserProfile(user=u)
        up.save()

# Start execution here!
if __name__ == '__main__':
    print "Starting go_fish population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech_project.settings')
    populate()

