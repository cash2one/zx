# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'www.misc.views.show_index_for_all_domain'),
                       url(r'^home$', 'www.account.views.show_index'),
                       url(r'^login$', 'www.account.views.login'),
                       url(r'^logout$', 'www.account.views.logout'),
                       url(r'^regist$', 'www.account.views.regist'),
                       url(r'^regist/(?P<invitation_code>\w+)$', 'www.account.views.regist'),
                       url(r'^reset_password$', 'www.account.views.reset_password'),
                       url(r'^forget_password$', 'www.account.views.forget_password'),
                       url(r'^qiniu_img_return$', 'www.misc.views.qiniu_img_return'),
                       url(r'^save_img$', 'www.misc.views.save_img'),
                       url(r'^crop_img$', 'www.misc.views.crop_img'),
                       url(r'^search_auto_complete$', 'www.question.views.search_auto_complete'),
                       url(r'^search$', 'www.question.views.search'),

                       url(r'^n/(?P<nick>.*)$', 'www.account.views.get_user_by_nick'),
                       url(r'^p/(?P<user_id>\w+)/?$', 'www.account.views.user_questions'),
                       url(r'^p/(?P<user_id>\w+)/questions/?$', 'www.account.views.user_questions'),
                       url(r'^p/(?P<user_id>\w+)/answers/?$', 'www.account.views.user_answers'),
                       url(r'^p/(?P<user_id>\w+)/following/?$', 'www.account.views.user_following'),
                       url(r'^p/(?P<user_id>\w+)/followers/?$', 'www.account.views.user_followers'),

                       url(r'^account/', include('www.account.urls')),
                       url(r'^question/', include('www.question.urls')),
                       url(r'^message/', include('www.message.urls')),
                       url(r'^timeline/', include('www.timeline.urls')),
                       url(r'^weixin/', include('www.weixin.urls')),
                       url(r'^zt/', include('www.zhuanti.urls')),
                       url(r'^kaihu/', include('www.kaihu.urls')),
                       url(r'^admin/', include('www.admin.urls')),
                       url(r'^stock/', include('www.stock.urls')),

                       url(r'^baidu_map$', 'www.misc.views.baidu_map'),
                       url(r'^baidu_map.html$', 'www.misc.views.baidu_map'),
                       url(r'^sitemap.xml$', 'www.misc.views.sitemap'),
                       # url(r'^8efc199540223825b0fb2026cc9b8e39\.html$', 'www.misc.views.link_view'),
                       url(r'^(?P<txt_file_name>\w+)\.txt$', 'www.misc.views.txt_view'),
                       url(r'^s/links$', 'www.misc.views.friendly_links'),
                       url(r'^s/(?P<template_name>.*)$', 'www.misc.views.static_view'),
                       url(r'^500$', 'www.account.views.test500'),
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
                       )

# 冗余url，用于减少url层级
urlpatterns += patterns('',
                        url(r'^topic/(?P<topic_domain>\w+)$', 'www.question.views.topic_question'),
                        url(r'^topics$', 'www.question.views.topics'),
                        url(r'^important/?$', 'www.question.views.important_question'),
                        )
