# -*- coding: utf-8 -*-
from odoo import http

# class Methods(http.Controller):
#     @http.route('/methods/methods/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/methods/methods/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('methods.listing', {
#             'root': '/methods/methods',
#             'objects': http.request.env['methods.methods'].search([]),
#         })

#     @http.route('/methods/methods/objects/<model("methods.methods"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('methods.object', {
#             'object': obj
#         })