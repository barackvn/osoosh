/* © 2016 Nedas Žilinskas <nedas.zilinskas@gmail.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
odoo.define('website_attachment.editor', function(require) {
    "use strict";

    var core = require('web.core');
    var website = require('website.website');
    var rpc = require('web.rpc');
    var options = require('web_editor.snippets.options');

    var _t = core._t;

    options.registry.website_attachment = options.Class.extend({

        on_prompt: function() {
            var self = this;
            return website.prompt({
                window_title: _t("Select Attachment Group"),
                select: _t("Attachment Group"),
                init: function(field) {
                    var current_id = parseInt(self.$target.attr('data-id'));
                    var select = field[0];
                    var model = new Model('x_attachment_group');
                    model.call('search_read', []).then(function(groups) {
                        for (var i in groups) {
                            var option_id = groups[i].id;
                            var option_name = groups[i].x_name;
                            var option_select = current_id == option_id ? true : false;
                            var option = new Option(option_name, option_id);
                            if (option_select) {
                                option.selected = true;
                            }
                            select.options[select.options.length] = option;
                        }
                    });
                },
            }).then(function(id) {
                self.$target.attr('data-id', id);
            });
        },

        drop_and_build_snippet: function() {
            var self = this;
            return self.on_prompt().fail(function() {
                self.editor.on_remove();
            });
        },

        switch_group: function(type) {
            if (type !== "click") return;

            return this.on_prompt();
        },

        clean_for_save: function() {
            this.$target.empty();
        }

    });
});