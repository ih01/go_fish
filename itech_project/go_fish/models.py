from django.db import models

from django.db import models

class User(models.Model):
    userID = models.CharField(max_length=15, unique=True)
    fishAmount = models.IntegerField(max_length=12)

    def __unicode__(self):
        return unicode(self.userID)

class Game(models.Model):
    user = models.ForeignKey(User)
    time = models.IntegerField(max_length=4)
    location = models.IntegerField(max_length=3)

    def __unicode__(self):
        return unicode(self.user)

class Items(models.Model):
    itemID = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=20)
    cost = models.IntegerField(max_length=5)
    fishMod = models.DecimalField(max_digits=5,decimal_places=2)
    timeMod = models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
        return unicode(self.name)

class Inventory(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Items)

    def __unicode__(self):
        return unicode(self.user) + ' - ' + unicode(self.item)
