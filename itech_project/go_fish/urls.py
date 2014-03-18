from django.conf.urls import patterns, url
from go_fish import views

urlpatterns = patterns('',
    url(r'^$', views.welcome, name='welcome'),
    #url(r'^welcome/', views.welcome, name='welcome'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^play/', views.play, name='play'),
    url(r'^help/', views.help, name='help'),
    url(r'^shop/', views.shop, name='shop'),
    url(r'^move/(?P<moveTo>\w+)/$', views.move, name='move'),
    url(r'buy/(?P<item>\w+)/$', views.buy, name='buy'),
    url(r'^profile/$', views.profile, name='profile'),
    )

