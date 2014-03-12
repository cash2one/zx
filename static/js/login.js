$(document).ready(function(){
    // 鼠标移动到第三方登录时的事件
    $('.img-hover').bind('mouseenter', function(){
        var me = $(this), type = me.data('type');
        me.animate({'opacity': '0.3'}, 200, function(){
            me.attr('src', '/static/img/common/'+type+'-active.png');
            me.animate({'opacity': '0.99'}, 200);
        });
    })
    .bind('mouseleave', function(){
        var me = $(this), type = me.data('type');
        me.animate({'opacity': '0.3'}, 200, function(){
            me.attr('src', '/static/img/common/'+type+'.png');
            me.animate({'opacity': '0.99'}, 200);
        });
    });

    // 登记按钮页面跳转
    $('.regist').bind('click', function(){
        window.location.href = '/regist';
    });
});