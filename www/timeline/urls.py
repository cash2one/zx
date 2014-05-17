# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# from django.conf import settings

urlpatterns = patterns('www.timeline.views',
                       url(r'^$', 'show_user_timeline'),
                       url(r'^get_user_timeline$', 'get_user_timeline'),
                       url(r'^follow/(?P<to_user_id>\w{32})$', 'follow_people'),
                       url(r'^unfollow/(?P<to_user_id>\w{32})$', 'unfollow_people'),
                       )
