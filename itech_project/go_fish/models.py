from django.db import models
from django.contrib.auth.models import User

class Rod(models.Model):
    name = models.CharField(max_length=20)
    cost = models.IntegerField(max_length=5)
    fishMod = models.DecimalField(max_digits=5,decimal_places=2)
    def __unicode__(self):
        return unicode(self.name)

class Boat(models.Model):
    name = models.CharField(max_length=20)
    cost = models.IntegerField(max_length=5)
    timeMod = models.DecimalField(max_digits=5,decimal_places=2)
    def __unicode__(self):
        return unicode(self.name)

class Bait(models.Model):
    name = models.CharField(max_length=20)
    cost = models.IntegerField(max_length=5)
    fishMod = models.DecimalField(max_digits=5,decimal_places=2)
    def __unicode__(self):
        return unicode(self.name)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    fishAmount = models.IntegerField(default=0)
    rod =  models.ForeignKey(Rod)
    boat = models.ForeignKey(Boat)
    bait = models.ForeignKey(Bait)
    def __unicode__(self):
        return unicode(self.user)

class Game(models.Model):
    user = models.ForeignKey(User)
    pickledgame = models.TextField()
    def __unicode__(self):
        return unicode(self.user)
