# -*- coding: utf-8 -*-

from django.db import models


class UnreadCount(models.Model):

    """
    @note: 用户的未读数提醒
    未读数字典信息，数据类型{'system_message':1, 'received_like':2, 'received_answer':3, 'at_answer':4}
    """
    user_id = models.CharField(max_length=32, unique=True)
    count_info = models.CharField(max_length=512)


class UnreadType(models.Model):

    """
    @note: 每一种提醒类型对应的具体信息
    """
    code = models.CharField(max_length=32, unique=True)  # 标示
    measure = models.CharField(max_length=8)  # 计量单位
    name = models.CharField(max_length=16)  # 名称
    url = models.CharField(max_length=128, default='')  # 对应的url
    href_name = models.CharField(max_length=32, default='')  # 超链接名称，如果超链需要的名称不同，可启用
    type = models.IntegerField(default=0)  # 类型，0代表临时通知，1代表通知消息，2代表请求, 3代表需要js操作的如posts

    def get_tips(self, count):
        """
        @note: 获取提示信息
        """
        count = int(count)
        pre = u'%s%s新%s，' % (count, self.measure, self.name)
        tips = u'%s<a href="%s">查看%s</a>' % (pre, self.url, self.name)
        return tips

    def __unicode__(self):
        return self.code


class Notice(models.Model):

    """
    @note: 通知信息
    """
    source_choices = ((0, u'默认消息'), (1, u''))

    user_id = models.CharField(max_length=32, db_index=True, null=True)  # 用户外键，可以为空，系统通知类
    content = models.CharField(max_length=128)  # 通知对应的内容
    source = models.CharField(max_length=32, choices=source_choices, default=0)  # 来源
    process_result = models.CharField(max_length=32, default='')  # 处理结果
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)  # 创建时间
    author_readed = models.BooleanField(default=False)  # 是否已读

    class Meta:
        ordering = ["-id"]


class InviteAnswer(models.Model):
    from_user_ids = models.TextField()
    to_user_id = models.CharField(max_length=32, db_index=True)
    question_id = models.CharField(max_length=32, db_index=True)

    is_read = models.BooleanField(verbose_name=u'是否已读', default=False)
    last_invite_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
        unique_together = [("to_user_id", 'question_id'), ]


class InviteAnswerIndex(models.Model):
    from_user_id = models.CharField(max_length=32, db_index=True)
    to_user_id = models.CharField(max_length=32, db_index=True)
    question_id = models.CharField(max_length=32)

    class Meta:
        unique_together = [("from_user_id", "to_user_id", 'question_id'), ]


class GlobalNotice(models.Model):

    """
    @note: 全站通告
    """
    level_choices = ((0, u'普通'), (1, u'必看'))
    platform_choices = ((0, u'全局'), (1, u'web端'), (2, u'手机端'))

    user_id = models.CharField(max_length=32, null=True)
    content = models.TextField()
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(db_index=True)
    level = models.IntegerField(default=0, choices=level_choices)
    platform = models.IntegerField(default=0, choices=platform_choices, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]
