odoo.define('website_shop_variant_desc.custom', function (require) {
"use strict";

require('web.dom_ready');
var ajax = require('web.ajax');


	$('#js_request_quote').on('click', function (ev) {
        var product_id = $(this).closest('form').find('.product_id').val();
        $("#request-quote-form .js_product_id").val(product_id);
    });

    $('#request-quote-form').on('submit', function (ev) {
        ev.preventDefault();
        var values = {};
        $("#request-quote-form").serializeArray().map(function(x){values[x.name] = x.value;}); 
         ajax.jsonRpc("/request-quote", 'call', {'values': values}).then(function(data){
         	$('#requestQuoteFormModal').modal('hide');
         	$('#request-quote-thank-you').removeClass('hidden');
         	$('#request-quote-submit').hide();
         });

    });

    $('.oe_website_sale').each(function () {
    	var oe_website_sale = this;
	    $(oe_website_sale).on('change', 'input.js_variant_change, select.js_variant_change, ul[data-attribute_value_ids]', function (ev) {
	    	var $ul = $(ev.target).closest('.js_add_cart_variants');
        	var $parent = $ul.closest('.js_product');
	    	var product_id = $parent.find('input.product_id').val();
	    	var toshow = '#' + product_id + '-desc-variant';

	    	$('#product_full_description').find('.shown').each(function () {
	    		$(this).removeClass('shown');
	    		$(this).addClass('hidden');
	    	});

	    	$(toshow).removeClass('hidden');
	    	$(toshow).addClass('shown');
	    });
	});

	$(document).ready(function () {
		if ($('.oe_website_sale').length) {
			var product_id = $('.js_add_cart_variants').find('input.product_id').val();
			var toshow = '#' + product_id + '-desc-variant';

			$(toshow).removeClass('hidden');
	    	$(toshow).addClass('shown');
		}
	});

});