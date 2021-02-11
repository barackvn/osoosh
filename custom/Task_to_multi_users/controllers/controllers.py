# -*- coding: utf-8 -*-
from openerp import http

# class TimesheetOnTask(http.Controller):
#     @http.route('/timesheet_on_task/timesheet_on_task/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/timesheet_on_task/timesheet_on_task/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('timesheet_on_task.listing', {
#             'root': '/timesheet_on_task/timesheet_on_task',
#             'objects': http.request.env['timesheet_on_task.timesheet_on_task'].search([]),
#         })

#     @http.route('/timesheet_on_task/timesheet_on_task/objects/<model("timesheet_on_task.timesheet_on_task"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('timesheet_on_task.object', {
#             'object': obj
#         })