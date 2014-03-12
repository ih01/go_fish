from models import UserProfile, Rod, Boat, Bait


class Shop(object):
    # constructor
    def __init__(self, amount):
        self.balance = amount

    # method for changing the balance in case of a purchase
    # updates item (rod, boat, bait) and balance in database
    def buyItem(self, item, user):

        if not ( self.balance > item.cost ):  # user has insufficient means
			return

        else:  # calculate new balance
			newBalance = self.balance - item.cost

			update = user.get_profile()

    # update user balance
        update.balance = newBalance

    # update database depending on the kind of item
        item_type = type(item)

        if item_type == type(Rod):
            update.rod = item
        elif item_type == type(Boat):
            update.boat = item
        elif item_type == type(Bait):
            update.bait = item
        else:
        print "error"