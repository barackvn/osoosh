# -*- coding: utf-8 -*-
from odoo import http

# class MissingFieldsAndViews(http.Controller):
#     @http.route('/missing_fields_and_views/missing_fields_and_views/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/missing_fields_and_views/missing_fields_and_views/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('missing_fields_and_views.listing', {
#             'root': '/missing_fields_and_views/missing_fields_and_views',
#             'objects': http.request.env['missing_fields_and_views.missing_fields_and_views'].search([]),
#         })

#     @http.route('/missing_fields_and_views/missing_fields_and_views/objects/<model("missing_fields_and_views.missing_fields_and_views"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('missing_fields_and_views.object', {
#             'object': obj
#         })
