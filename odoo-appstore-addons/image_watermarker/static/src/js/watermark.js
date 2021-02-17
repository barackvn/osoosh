odoo.define('image_watermarker.image_watermarker_js', function(require) {
    'use strict';

    var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');

    //  Products Layout Views..........................................
    publicWidget.registry.watermark = publicWidget.Widget.extend({
        selector: '#wrapwrap',
        willStart:function(){
            var self = this;
            return ajax.jsonRpc('/watermark/last/update/on',{}).then (function(res){
                if(res){
                    self.updated_on = res.update_list;
                }
                else{
                    self.updated_on = "";
                }
            });
        },
        start:function(){
            
            console.log(" self.updated_on", this.updated_on);
            localStorage.setItem('updated_on', "1");
            // document.getElementById("container").src += `?v=${new Date().getTime()}`;


        }

    });
});