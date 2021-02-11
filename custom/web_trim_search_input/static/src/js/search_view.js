odoo.define('web_trim_search_view.SearchView', function (require) {
"use strict";

var AutoComplete = require('web.AutoComplete');
var SearchView = require('web.SearchView');

SearchView.include({
    setup_global_completion: function () {
        var self = this;
        this.autocomplete = new AutoComplete(this, {
            source: this.proxy('complete_global_search'),
            select: this.proxy('select_completion'),
            get_search_string: function () {
                return self.$('.o_searchview_input').val().trim();
            },
        });
        this.autocomplete.appendTo(this.$('.o_searchview_input_container'));
    },
});

});

