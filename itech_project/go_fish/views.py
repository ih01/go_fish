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
from user_item_control import *
from shop import Shop
from django.contrib.auth.models import User


def welcome(request):
    context = RequestContext(request)
    context_dict = check_user(request)
    return render_to_response('welcome.html', context_dict, context)


def help(request):
    context = RequestContext(request)
    context_dict = check_user(request)
    return render_to_response('help.html', context_dict, context)


# hopefully won't need seperate page for this

def register(request):
    context = RequestContext(request)
    profile = None
    registered = False  #boolean indicating success of registration
    #process
    if request.method == 'POST':
        #try to get info from raw form
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        #if valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)  #hash password
            user.save()  #update user object
            initial_rod = getRod(1)
            initial_boat = getBoat(1)
            initial_bait = getBait(1)
            profile = profile_form.save(commit=False)  #userprofile instance
            profile.rod = initial_rod
            profile.boat = initial_boat
            profile.bait = initial_bait
            profile.user = user
            new_game(user)
            #  if 'picture' in request.FILES:
            #profile.picture = request.FILES['picture']
            profile.save()
            registered = True
            #log newly registered user in straight away
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, user)
        else:
            print user_form.errors, profile_form.errors
            return HttpResponse("Invalid registration details supplied.Please go back and try again.")
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
        'register.html',
        {'user_form': user_form, 'user_profile': profile, 'profile_form': profile_form, 'registered': registered},
        context)


def user_login(request):
    context = RequestContext(request)
    user_prof = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                return HttpResponse("Your Go Fish account has been disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied. Please go back and try again.")
    else:
        return render_to_response('login.html', {}, context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required
def play(request):
    context = RequestContext(request)
    us = request.user
    user_prof = get_userProfile(us)
    game = load_game(us)
    coords = str(game.get_X()) + "_" + str(game.get_Y())
    return render_to_response('Play.html', {'user_profile': user_prof, 'game': game, 'coords': coords}, context)


@login_required
def move(request, moveTo):
    context = RequestContext(request)
    context_dict = {}
    context_dict['moveTo'] = moveTo
    us = request.user
    game = load_game(us)
    moveX = int(moveTo[0])
    moveY = int(moveTo[2])
    if moveX == game.get_X() and moveY == game.get_Y():
        baitMod = get_baitMod(us)
        rodMod = get_rodMod(us)
        fishCaught = game.fish(rodMod, baitMod)
    else:
        boatMod = get_boatMod(us)
        game.move(moveX, moveY, boatMod)
        fishCaught = 0
    context_dict['fishCaught'] = fishCaught
    save_game(us, game)
    game_over = check_end_game(us, game)
    context_dict['game'] = game
    context_dict['Game_Over'] = game_over
    coords = str(game.get_X()) + "_" + str(game.get_Y())
    user_prof = get_userProfile(us)
    context_dict['user_profile'] = user_prof
    context_dict['coords'] = coords
    return render_to_response('Play.html', context_dict, context)


@login_required
def shop(request):
    context = RequestContext(request)
    us = request.user
    game = load_game(us)
    fishToMoney(us, game)
    save_game(us, game)
    user_profile = get_userProfile(us)
    rod_list = get_rodList(us)
    boat_list = get_boatList(us)
    bait_list = get_baitList(us)
    context_dict = {'rods': rod_list, 'boats': boat_list, 'bait': bait_list, 'user_profile': user_profile}
    return render_to_response('shop.html', context_dict, context)


@login_required
def buy(request, item):
    context = RequestContext(request)
    item_level = item[0]
    item_type = item[1]

    if item_type == 'R':
        new_item = getRod(item_level)
    elif item_type == 'B':
        new_item = getBoat(item_level)
    elif item_type == 'b':
        new_item = getBait(item_level)
    else:
        print "error"

    user = request.user
    new_shop = Shop()
    new_shop.buyItem(new_item, user)
    user_profile = get_userProfile(user)
    rod_list = get_rodList(user)
    boat_list = get_boatList(user)
    bait_list = get_baitList(user)
    context_dict = {'rods': rod_list, 'boats': boat_list, 'bait': bait_list, 'user_profile': user_profile}

    if user_profile.balance_status is False:
        return render_to_response('balance_error.html')
    else:
        return render_to_response('shop.html', context_dict, context)


@login_required
def profile(request):
    context = RequestContext(request)
    context_dict = {}
    #u = User.objects.get(username=request.user)
    u = request.user

    try:
        #up = UserProfile.objects.get(user=u)
        up = get_userProfile(u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['user_profile'] = up
    return render_to_response('profile.html', context_dict, context)


@login_required
def restricted(request):
    return HttpResponse("this is restricted...")
