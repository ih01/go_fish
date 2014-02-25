import os

def populate():
    
    add_item(id="1",
        name="Wooden Fishing Rod",
        cost="0",
	fishMod="1",
	timeMod="0")

    add_item(id="2",
        name="Iron Fishing Rod",
        cost="50",
	fishMod=".1",
	timeMod="0")

    add_item(id="3",
        name="Steel Fishing Rod",
        cost="150",
	fishMod=".25",
	timeMod="0")

    add_item(id="4",
        name="Mithril Fishing Rod",
        cost="300",
	fishMod=".5",
	timeMod="0")

# can add in other items like this easily
# not sure what Itemid is in the models - thought this would be the item category, but is unique in the models?

def add_item(id, name, cost, fishMod, timeMod):
    i = Items.objects.get_or_create(itemID=id, name=name, cost=cost, fishMod=fishMod, timeMod=timeMod)[0]
    return i

# Start execution here!
if __name__ == '__main__':
    print "Starting go_fish population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech_project.settings')
    from go_fish.models import Items
    populate()

