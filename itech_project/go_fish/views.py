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
from models import Rod, Boat, Bait, Game, UserProfile
from shop import Shop
from django.contrib.auth.models import User


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
            if 'picture' in request.FILES:
               profile.picture = request.FILES['picture']

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
    context = RequestContext(request)
    us = request.user
    user_prof = UserProfile.objects.get(user=us)
    game = load_game(us)
    coords = int(str(game.posX) + str(game.posY))
    return render_to_response('Play.html', {'user_prof':user_prof, 'game':game, 'coords':coords},context)

def fish(request):
    context = RequestContext(request)
    us = request.user
    user_prof = UserProfile.objects.get(user=us)
    game = load_game(us)
    baitMod = get_baitMod(us)
    rodMod = get_rodMod(us)
    fishCaught = game.fish(rodMod, baitMod)
    save_game(us, game)
    game_over = check_end_game(us, game)
    coords = int(str(game.get_X()) + str(game.get_Y()))
    return render_to_response('Play.html', {'user_prof':user_prof, 'game':game, 'fishCaught':fishCaught, 'coords':coords, 'Game_Over':game_over},context)

def move(request, moveTo):
    context = RequestContext(request)
    us = request.user
    user_prof = UserProfile.objects.get(user=us)
    game = load_game(us)
    moveX= int(moveTo[0])
    moveY= int(moveTo[1])
    boatMod = get_boatMod(us)
    game.move(moveX, moveY, boatMod)
    save_game(us, game)
    game_over = check_end_game(us, game)
    coords = int(str(game.get_X()) + str(game.get_Y()))
    return render_to_response('Play.html', {'user_prof':user_prof, 'game':game, 'coords':coords, 'moveTo': moveTo, 'Game_Over':game_over},context)

def help(request):
    return HttpResponse("Placeholder for help page")

def shop(request):
    context = RequestContext(request)
    user_profile = UserProfile.objects.get(user=request.user)
    rod_list = Rod.objects.filter(level__gt=user_profile.rod.level)
    boat_list = Boat.objects.filter(level__gt=user_profile.boat.level)
    bait_list = Bait.objects.filter(level__gt=user_profile.bait.level)
    context_dict = {'rods': rod_list, 'boats': boat_list, 'bait': bait_list, 'user_profile': user_profile}
    return render_to_response('shop.html', context_dict, context)

def buy(request, item):
    item_level = item[0]
    item_type = item[1]

    if item_type == 'R':
        new_item = Rod.objects.get(pk=int(item_level))
    elif item_type == 'B':
        new_item = Boat.objects.get(pk=int(item_level))
    elif item_type == 'b':
        new_item = Bait.objects.get(pk=int(item_level))
    else:
         print "error"

    user = request.user
    new_shop = Shop()
    new_shop.buyItem(new_item, user)
    user_profile = UserProfile.objects.get(user=user)
    rod_list = Rod.objects.filter(level__gt=user_profile.rod.level)
    boat_list = Boat.objects.filter(level__gt=user_profile.boat.level)
    bait_list = Bait.objects.filter(level__gt=user_profile.bait.level)
    context_dict = {'rods': rod_list, 'boats': boat_list, 'bait': bait_list, 'user_profile': user_profile}

    return render_to_response('shop.html', context_dict)


@login_required
def profile(request):
    context = RequestContext(request)
    context_dict = {}
    u = User.objects.get(username=request.user)

    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('profile.html', context_dict, context)

@login_required
def restricted(request):
    return HttpResponse("this is restricted...")
