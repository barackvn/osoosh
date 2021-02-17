/* © 2016 Nedas Žilinskas <nedas.zilinskas@gmail.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
odoo.define('website_attachment.main', function(require) {
    "use strict";

    var session = require('web.session');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');
    var animation = require('website.content.snippets.animation');

    var qweb = core.qweb;

    var WebsiteSaleAttachmentGroup = Widget.extend({
        events: {},
        init: function(parent, id) {
            this.template = 'website_attachment.s_attachment_group_' + id;
            this._super(parent);
        },
    });

    animation.registry.website_attachment = animation.Class.extend({
        selector: ".website_attachment",
        widget: null,
        start: function() {
            var def = this._super.apply(this, arguments);
            if (this.editableMode) {
                return def;
            }

            var self = this;
            var target = self.$target.empty();
            var id = parseInt(target.attr('data-id'));

            if (!id) {
                console.log(id, target.attr('data-id'))
                return def;
            }

            return ajax.loadXML('/website/action/website_attachment/' + id, qweb).then(function() {
                self.widget = new WebsiteSaleAttachmentGroup(self, id);
                self.widget.appendTo(target);
            });

        },
        stop: function() {
            this.widget.destroy();
        }
    });

});