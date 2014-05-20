$(document).ready(function(){
	var Log = Backbone.Model.extend({
		defaults: {
			'year': '2014年',
			'date': '05月05日',
			'contents': []
		}
	});

	var Logs = Backbone.Collection.extend({
		model: Log,

		setData: function(){
			this.reset([
				{'count': 3, 'year': '2014年', 'date': '05月12日', 'contents': _.map([
					'新增关注用户功能',
					'新增话题广场',
					'新增用户名片、话题名片功能',
					'新增时间线功能，显示关注用户动态信息',
                    '优化手机、平板访问体验'
				], function(content){return String.format('<li><p>{0}</p></li>', content)}).join('')},

				{'count': 2, 'year': '2014年', 'date': '04月06日', 'contents': _.map([
					'新增提问回答分享到微博、腾讯QQ',
					'新增分享赞到微博、腾讯QQ',
					'新增上传头像裁剪功能',
					'文本编辑器优化',
					'开放智选日报公众号，扫描二维码关注',
					'开放智选交流群: 375931749',
					'开放<a class="co3 pl-5" target="_blank" href="http://weibo.com/zhixuancom">智选官方微博</a>'
				], function(content){return String.format('<li><p>{0}</p></li>', content)}).join('')},

				{'count': 1, 'year': '2014年', 'date': '03月12日', 'contents': _.map([
					'智选横空出世，正式开放内测'
				], function(content){return String.format('<li><p>{0}</p></li>', content)}).join('')}
			]);

		}
	});

	var LogView = Backbone.View.extend({
		el: '.logs',

		template: _.template($('#log-template').html()),

		initialize: function(){
			this.listenTo(this.collection, 'reset', this.render);

			this.collection.setData();
		},

		render: function(){
			this.$el.html(
				this.template(
					{'logs': this.collection.toJSON()}
				)
			);

			// 设置波纹
			this.$('.hidden-xs').eq(0).append('<span class="wave"></span>');
		}
	});

	var logs = new Logs(),
		logView = new LogView({collection: logs});
});