from django.conf.urls import patterns, url
from go_fish import views

urlpatterns = patterns('',
        url(r'^welcome/', views.welcome, name='welcome'),
	url(r'^register/', views.register, name='register'),
        url(r'^play/', views.play, name='play'),
        url(r'^shop/', views.shop, name='shop'),)
