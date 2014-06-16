# -*- coding: utf-8 -*-
import json
import logging

from django.http import HttpResponse  # , HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from common import utils, page, debug, user_agent_parser
from www.misc import qiniu_client
from www.misc.decorators import member_required, common_ajax_response
from www.tasks import async_clear_count_info_by_code
from www.account import interface as interface_account
from www.question import interface as interface_question
from www.message import interface


urb = interface.UnreadCountBase()
lb = interface_question.LikeBase()
ab = interface_question.AnswerBase()
ub = interface_account.UserBase()
iab = interface.InviteAnswerBase()


@member_required
def system_message(request, template_name='message/system_message.html'):
    system_messages = urb.get_system_message(request.user.id)

    # 分页
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(system_messages, count=10, page=page_num).info
    system_messages = page_objs[0]
    page_params = (page_objs[1], page_objs[4])

    # 异步清除未读消息数
    async_clear_count_info_by_code(request.user.id, code='system_message')
    unread_count_info = urb.get_unread_count_info(request.user)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def received_like(request, template_name='message/received_like.html'):

    likes = lb.get_to_user_likes(request.user.id)

    # 分页
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(likes, count=10, page=page_num).info
    likes = page_objs[0]
    page_params = (page_objs[1], page_objs[4])
    likes = lb.format_likes(likes)
    likes_count = page_objs[5]

    # 异步清除未读消息数
    async_clear_count_info_by_code(request.user.id, code='received_like')
    unread_count_info = urb.get_unread_count_info(request.user)

    user_agent_dict = user_agent_parser.Parse(request.META.get('HTTP_USER_AGENT'))

    # 手机客户端换模板
    if user_agent_dict['os']['family'] in ('Android', 'iOS'):
        template_name = 'message/received_like_m.html'

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def received_answer(request, template_name='message/received_answer.html'):
    answers = ab.get_user_received_answer(request.user.id)

    # 分页
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(answers, count=10, page=page_num).info
    answers = page_objs[0]
    page_params = (page_objs[1], page_objs[4])
    answers = ab.format_answers(answers)

    # 异步清除未读消息数
    async_clear_count_info_by_code(request.user.id, code='received_answer')
    unread_count_info = urb.get_unread_count_info(request.user)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def at_answer(request, template_name='message/at_answer.html'):
    answers = ab.get_at_answers(request.user.id)

    # 分页
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(answers, count=10, page=page_num).info
    answers = page_objs[0]
    page_params = (page_objs[1], page_objs[4])
    answers = ab.format_answers(answers)

    # 异步清除未读消息数
    async_clear_count_info_by_code(request.user.id, code='at_answer')
    unread_count_info = urb.get_unread_count_info(request.user)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def invite_answer(request, template_name='message/invite_answer.html'):
    user_received_invites = iab.get_user_received_invite(to_user_id=request.user.id)

    # 分页
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(user_received_invites, count=10, page=page_num).info
    user_received_invites = page_objs[0]
    page_params = (page_objs[1], page_objs[4])
    user_received_invites = iab.format_user_received_invites(user_received_invites)

    # 异步清除未读消息数
    async_clear_count_info_by_code(request.user.id, code='invite_answer')
    unread_count_info = urb.get_unread_count_info(request.user)

    # 设置邀请回答未读状态，根据第一条记录来判读
    if user_received_invites and not user_received_invites[0].is_read:
        iab.update_invite_is_read(request.user.id)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

# ===================================================ajax部分=================================================================#


@member_required
def get_unread_count_total(request):
    count_info = urb.get_unread_count_total(request.user)

    # 更新最后活跃时间
    ub.update_user_last_active_time(request.user.id, ip=utils.get_clientip(request))
    return HttpResponse(json.dumps(count_info), mimetype='application/json')


def show_received_like(request, template_name='message/show_received_like.html'):
    '''
    显示指定用户收到的赞列表 用于分享  无需登录
    '''
    user_id = request.REQUEST.get('user_id')
    if not user_id:
        return render_to_response(template_name, locals(), context_instance=RequestContext(request))

    user = ub.get_user_by_id(user_id)
    if not user:
        return render_to_response(template_name, locals(), context_instance=RequestContext(request))

    request.user = user

    likes = lb.get_to_user_likes(request.user.id)

    # 分页
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(likes, count=10, page=page_num).info
    likes = page_objs[0]
    page_params = (page_objs[1], page_objs[4])
    likes = lb.format_likes(likes)
    likes_count = page_objs[5]

    # 异步清除未读消息数
    async_clear_count_info_by_code(request.user.id, code='received_like')
    unread_count_info = urb.get_unread_count_info(request.user)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def share_received_like(request):
    '''
    后台生成分享的图片
    '''
    import os
    from django.conf import settings

    result = {'flag': -1, 'result': '操作失败'}

    # 拼装获取指定用户赞的页面url
    url = "%s://%s/message/show_received_like?user_id=%s" % (
        request.META['wsgi.url_scheme'],
        'wwwinside.zhixuan.com',
        # request.META['HTTP_HOST'],
        request.user.id
    )

    # 定义生成临时图片位置
    file_name = '%s/static_local/temp_share/capty_%s.png' % (os.path.dirname(settings.SITE_ROOT), utils.uuid_without_dash())
    temp = None

    try:
        # 调用子程序 生成图片
        #cmd = 'python %s/common/capty.py %s %s' % (os.path.dirname(settings.SITE_ROOT), url, file_name)
        #cmd = 'python %s/common/_webkit2png.py -x 1366 768 -g 1366 0 -o %s %s' % (os.path.dirname(settings.SITE_ROOT), file_name, url)
        cmd = '/opt/python2.7.2/bin/python2.7 %s/common/_webkit2png.py -x 1366 768 -g 1366 0 -o %s %s' % (os.path.dirname(settings.SITE_ROOT), file_name, url)
        flag, msg = utils.exec_command(cmd, 20)
        logging.error(u'cmd is:\n%s\n msg is:%s' % (cmd, msg))
        if not flag:
            result = {'flag': -1, 'result': u'服务器响应超时, 请重试'}
        else:
            # 读取临时文件上传到七牛
            temp = open(file_name, 'rb')
            flag, img_name = qiniu_client.upload_img(temp)
            if flag:
                result = {'flag': 0, 'result': '%s/%s' % (settings.IMG0_DOMAIN, img_name.split('!')[0])}
            else:
                result = {'flag': -1, 'result': u'分享失败, 请重试'}
    except Exception, e:
        logging.error(debug.get_debug_detail(e))
        result = {'flag': -1, 'result': u'分享失败, 请重试'}
    finally:
        # 善后
        if temp:
            temp.close()
            os.remove(file_name)

    return HttpResponse(json.dumps(result), mimetype='application/json')


@member_required
def show_invite_user(request):
    from www.account.interface import UserCountBase

    question_id = request.REQUEST.get('question_id', '').strip()

    show_invite_users = UserCountBase().get_show_invite_users(exclude_user_id=request.user.id)
    invited_users = iab.get_invited_user_by_question_id(request.user.id, question_id)
    show_invite_users, invited_users = iab.format_invite_user(show_invite_users, invited_users)

    data = dict(invited_users=invited_users, show_invite_users=show_invite_users)
    return HttpResponse(json.dumps(data), mimetype='application/json')


@member_required
@common_ajax_response
def invite_user_answer(request):
    to_user_id = request.POST.get('to_user_id', '').strip()
    question_id = request.POST.get('question_id', '').strip()
    return iab.create_invite(request.user.id, to_user_id, question_id)


@member_required
def get_all_valid_global_notice(request):
    gnb = interface.GlobalNoticeBase()
    global_notice = gnb.format_global_notice(gnb.get_all_valid_global_notice())
    return HttpResponse(json.dumps(global_notice), mimetype='application/json')
