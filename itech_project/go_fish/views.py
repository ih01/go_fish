from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from game_control import *
from game import MakeGame
from go_fish.models import Rod, Boat, Bait, Game, UserProfile

def welcome(request):

    context = RequestContext(request)

    context_dict = {}

    return render_to_response('welcome.html', context_dict, context)

# hopefully won't need seperate page for this

def register(request):
    context = RequestContext(request)
    registered = False       #boolean indicating success of registration

    #process
    if request.method == 'POST':
        #try to get info from raw form
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #if valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)                 #hash password
            user.save()                                      #update user object

            initial_rod = Rod.objects.get(name='Wooden Fishing Rod')
            initial_boat = Boat.objects.get(name='Raft')
            initial_bait = Bait.objects.get(name='Worm')
            profile = profile_form.save(commit=False)        #userprofile instance
            profile.rod = initial_rod
            profile.boat = initial_boat
            profile.bait = initial_bait

            profile.user = user
            new_game(user)
           # if 'picture' in request.FILES:
               # profile.picture = request.FILES['picture']

            profile.save()
            registered = True
            #log newly registered user in straight away
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, user)

        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
        'register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)
   # return HttpResponse("Placeholder for register page")

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/go_fish/welcome/')
            else:
                return HttpResponse("Your Go Fish account has been disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/go_fish/welcome/')


def play(request):
    us = request.user
    user_prof = UserProfile.objects.get(user=us)
    game = load_game(us)
    coords = int(str(game.posX) + str(game.posY))
    return render_to_response('Play.html', {'user_prof':user_prof, 'game':game, 'coords':coords})

def fish(request):
    us = request.user
    user_prof = UserProfile.objects.get(user=us)
    game = load_game(us)
    baitMod = get_baitMod(us)
    rodMod = get_rodMod(us)
    fishCaught = game.fish(rodMod, baitMod)
    save_game(us, game)
    game_over=False
    if (game.get_time())<1:
	fishToMoney(us, game)
	reset_game(us)
	game_over=True
    coords = int(str(game.get_X()) + str(game.get_Y()))
    return render_to_response('Play.html', {'user_prof':user_prof, 'game':game, 'fishCaught':fishCaught, 'coords':coords, 'Game_Over':game_over})

def move(request, moveTo):
    us = request.user
    user_prof = UserProfile.objects.get(user=us)
    game = load_game(us)
    moveX= int(moveTo[0])
    moveY= int(moveTo[1])
    boatMod = get_boatMod(us)
    game.move(moveX, moveY, boatMod)
    save_game(us, game)
    game_over=False
    if (game.get_time())<1:
	fishToMoney(us, game)
	reset_game(us)
	game_over=True
    coords = int(str(game.get_X()) + str(game.get_Y()))
    return render_to_response('Play.html', {'user_prof':user_prof, 'game':game, 'coords':coords, 'moveTo': moveTo, 'Game_Over':game_over})

def help(request):
    return HttpResponse("Placeholder for help page")
def shop(request):
    return HttpResponse("Placeholder for shop page")

@login_required
def restricted(request):
    return HttpResponse("this is restricted...")
