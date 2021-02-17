odoo.define('website_event_cert_shop.datepicker', function(require) {
    // 'use strict';

    var ajax = require('web.ajax');
    var Modernizr = window.Modernizr;

    $(document).ready(function () {
        if (!Modernizr.inputtypes.date) {
            $('input[type=date]').datepicker({
                  dateFormat : 'yy-mm-dd'
                }
             );
        }
    });

});