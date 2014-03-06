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

from go_fish.models import Rod, Boat, Bait, Game

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
           # if 'picture' in request.FILES:
               # profile.picture = request.FILES['picture']

            profile.save()
            registered = True

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
    context = RequestContext(request, {})
    session_id = request.session._get_or_create_session_key()
    us = request.user
    game = new_game(us)
    coords = int(str(game.posX) + str(game.posY))
    return render_to_response('Play.html', {'us':us, 'game':game, 'coords':coords})

def fish(request):
    context = RequestContext(request, {})
    us = request.user
    game = load_game(us)
    fishCaught = game.fish(us)
    save_game(us, game)
    coords = int(str(game.posX) + str(game.posY))
    return render_to_response('Play.html', {'us':us, 'game':game, 'fishCaught':fishCaught, 'coords':coords})

def move(request, moveTo):
    context = RequestContext(request, {})
    us = request.user
    game = load_game(us)
    moveX= int(moveTo[0])
    moveY= int(moveTo[1])
    save_game(us, game)
    game.move(us, moveX, moveY)
    save_game(us, game)
    coords = int(str(game.posX) + str(game.posY))
    return render_to_response('Play.html', {'us':us, 'game':game,  'coords':coords, 'moveTo': moveTo})

def help(request):
    return HttpResponse("Placeholder for help page")
def shop(request):
    return HttpResponse("Placeholder for shop page")

@login_required
def restricted(request):
    return HttpResponse("this is restricted...but you can see it because you are cool!")
