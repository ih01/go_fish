import os
from itech_project import settings
from django.core.management import setup_environ
setup_environ(settings)
from go_fish.models import Bait, Rod, Boat, UserProfile, Game
from django.contrib.auth.models import User

def populate():
   
# Add item data here

	# Rods
	rod1=add_rod(name="Wooden Fishing Rod",
	cost="0",
	fishMod="2")
	
	rod2=add_rod(name="Iron Fishing Rod",
	cost="100",
	fishMod="4")
	
	rod3=add_rod(name="Steel Fishing Rod",
	cost="500",
	fishMod="6")

	rod4=add_rod(name="Mithril Fishing Rod",
	cost="1000",
	fishMod="8")
	
	# Boats	
	boat1=add_boat(name="Raft",
	cost="0",
	timeMod="2")
	
	boat2=add_boat(name="Kayak",
	cost="100",
	timeMod="4")

	boat3=add_boat(name="Motor boat",
	cost="500",
	timeMod="6")
	
	boat4=add_boat(name="Speed boat",
	cost="1000",
	timeMod="8")

	# Baits	
	bait1=add_bait(name="Worm",
	cost="0",
	fishMod="1")
	
	bait2=add_bait(name="Basic Lure",
	cost="60",
	fishMod="2")

	bait3=add_bait(name="Advanced Lure",
	cost="300",
	fishMod="3")
	
	bait4=add_bait(name="Bucket O'Bait",
	cost="600",
	fishMod="4")

# Sample User Data

	player1=add_player("Fischer Mann", "Test", rod1, boat2, bait1, "600")
	player2=add_player("Salty Sea Dog", "Test", rod4, boat4, bait3, "5000")
	

# Sample game Data

	add_game(player1, "yjcfck")
	add_game(player2, "lhjb")
	
  
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

def add_player(name, pw, rod1, boat1, bait1, fish):

    email = '{0}@{1}.com'.format(name,name)
    try:
        u = User.objects.get(username=name)
    except:
        u = User(username=name, email=email)
        u.set_password(pw)
        u.save()
        up = UserProfile(user=u, fishAmount=fish, rod=rod1, boat=boat1, bait=bait1)
        up.save()
    return u

# Start execution here!
if __name__ == '__main__':
    print "Starting go_fish population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech_project.settings')
    populate()

