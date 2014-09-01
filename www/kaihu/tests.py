# -*- coding: utf-8 -*-

import os
import sys

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
# 引入父目录来引入其他模块
sys.path.extend([os.path.abspath(os.path.join(SITE_ROOT, '../')),
                 os.path.abspath(os.path.join(SITE_ROOT, '../../')),
                 ])
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'


user_id = user = 'f762a6f5d2b711e39a09685b35d0bf16'


def main():
    from www.kaihu import interface
    cmb = interface.CustomerManagerBase()
    flb = interface.FriendlyLinkBase()
    cb = interface.CityBase()

    # print cmb.add_customer_manager(user_id, 2082, end_date='2014-06-01')
    # print flb.add_friendly_link(name=u'163', href='http://www.163.com', link_type=0, city_id=1932)
    # print flb.get_friendly_link_by_city_id(city_id=1932)

    atb = interface.ArticleBase()
    # atb.add_article(u"手游概念股有哪些？页游，端游呢？", u"asdfasdfasdfads", city_id="1932")
    print cb.get_city_baidu_rank(2001)


if __name__ == '__main__':
    main()
