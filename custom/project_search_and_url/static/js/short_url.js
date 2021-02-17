odoo.define('project_search_and_url.short_url', function (require) {
"use strict";

var core = require('web.core');
var FormWidgets = require('web.form_widgets')

var FieldShortUrl = FormWidgets.FieldEmail.extend({

    render_value: function() {
        this._super();
        if(this.get("effective_readonly")) {
            var tmp = this.get('value');
            var s = /(\w+):(.+)|^\.{0,2}\//.exec(tmp);
            if (!s) {
                tmp = "http://" + this.get('value');
            }
            this.$el.attr('href', tmp).text("More Information URL Link");
        }
    }
});

core.form_widget_registry
	.add('short_url', FieldShortUrl);
});