from models import UserProfile, Rod, Boat, Bait

import os
from itech_project import settings
from django.core.management import setup_environ
setup_environ(settings)

class Shop(object):
    # constructor
    def __init__(self):
        """


        """

    # method for changing the balance in case of a purchase
    # updates item (rod, boat, bait) and balance in database
    def buyItem(self, item, user):

        update = UserProfile.objects.get(user=user)

        if not ( update.balance > item.cost ):  # user has insufficient means
            return

        else:  # calculate new balance
            newBalance = update.balance - item.cost



        # update user balance
            update.balance = newBalance

        # update database depending on the kind of item
            item_type = item.type

            print item_type

            if item_type == 'Rod':
                update.rod = item
            elif item_type == 'Boat':
                update.boat = item
            elif item_type == 'Bait':
                update.bait = item
            else:
                print "error"

            update.save()