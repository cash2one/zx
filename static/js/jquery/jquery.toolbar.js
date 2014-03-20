/**
 * Toolbar.js
 *
 * @fileoverview  jQuery plugin that creates tooltip style toolbars.
 * @link          http://paulkinzett.github.com/tooltip-toolbar/
 * @author        Paul Kinzett (http://kinzett.co.nz/)
 * @version       1.0.0
 * @requires      jQuery 1.7+
 *
 * @license jQuery Toolbar Plugin v1.0.0
 * http://paulkinzett.github.com/tooltip-toolbar/
 * Copyright 2013 Paul Kinzett (http://kinzett.co.nz/)
 * Released under the MIT license.
 * <https://raw.github.com/paulkinzett/tooltip-toolbar/master/LICENSE.txt>
 */

if ( typeof Object.create !== 'function' ) {
    Object.create = function( obj ) {
        function F() {};
        F.prototype = obj;
        return new F();
    };
};

(function( $, window, document, undefined ) {
    
    var ToolBar = {
        init: function(options, elem, afterShowFun) {
            var self = this;

            self.elem = elem;
            self.$elem = $( elem );
            self.afterShowFun = afterShowFun;

            self.options = $.extend( {}, $.fn.toolbar.options, options );
            self.toolbar = $('<div class="tool-container gradient" />')
            .addClass('tool-'+self.options.position)
            .append('<div class="tool-items" />')
            .append('<div class="arrow" />')
            .appendTo('body')
            .hide()            

            self.initializeToolbar();
        },
        
        initializeToolbar: function() {
            var self = this;
            self.populateContent();           
            self.setTrigger();
        },
        
        setTrigger: function() {
            var self = this;
            
            self.$elem.on('click', function(event) {
                event.preventDefault();
                event.stopPropagation();
                if(self.$elem.hasClass('pressed')) {
                    self.hide();
                } else {
                    self.show();
                }
            });   

            $(window).resize(function( event ) {
                event.stopPropagation();
                css = self.getCoordinates(self.options.position, 20);
                self.toolbar.stop().animate(css);
            });

            // 点击任何地方关闭
            $('body').bind('click', function(e){
                self.hide();
            })
        },
        
        populateContent: function() {
            var self = this;
            var location = self.toolbar.find('.tool-items');
            var content = $(self.options.content).clone().find('a').addClass('tool-item gradient');
            location.html(content);            
        },
        
        calculatePosition: function() {
            var self = this;  
            css = self.getCoordinates(self.options.position, 5);
            css.position = 'absolute';
            css.zIndex = 120;            
            self.toolbar.css(css);
        },
        
        getCoordinates: function( position, adjustment) {
            var self = this; 
            self.coordinates = {
                top: self.$elem.offset().top + ($.browser.msie ? document.documentElement.scrollTop : 0),
                left: self.$elem.offset().left
            };
            if(position == 'top') { 
                return coordinates = {
                    left: self.coordinates.left-(self.toolbar.width()/2)+(self.$elem.width()/2),
                    top: self.coordinates.top-self.$elem.height()-adjustment,
                }
            }

            if(position == 'left') { 
                return coordinates = {
                    left: self.coordinates.left-(self.toolbar.width()/2)-(self.$elem.width()/2)-adjustment,
                    top: self.coordinates.top-(self.toolbar.height()/2)+(self.$elem.height()/2),
                }
            }

        },

        show: function() {
            var self = this;
  
            self.$elem.addClass('pressed');
            self.calculatePosition();

            var animation = {
                'opacity': 1,
            };

            if(self.options.position == 'top') {
                animation.top = '-=20';
            }

            if(self.options.position == 'left') {
                animation.left = '-=20';
            }            

            self.toolbar.show().animate(animation, 200 );

            // 显示之后的回调函数
            if(self.afterShowFun){
                self.afterShowFun(self.$elem);
            }
        },

        hide: function() {
            var self = this;
            self.$elem.removeClass('pressed');
            var animation = {
                'opacity': 0,
            };

            if(self.options.position == 'top') {
                animation.top = '+=20';
            }

            if(self.options.position == 'left') {
                animation.left = '+=20';
            }             
            self.toolbar.animate(animation, 200, function() {
                self.toolbar.hide();
            } );
        },        

    }
    
    $.fn.toolbar= function( options, afterShowFun) {      
        return this.each(function() {
            var toolbarObj = Object.create( ToolBar );
            toolbarObj.init( options, this, afterShowFun);
        });
    };    
    
    $.fn.toolbar.options = {
        content: '#myContent',
        position: 'top'
    };    
    
    
}) ( jQuery, window, document );