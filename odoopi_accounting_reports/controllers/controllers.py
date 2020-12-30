# -*- coding: utf-8 -*-
# from odoo import http


# class OdoopiAccountingReports(http.Controller):
#     @http.route('/odoopi_accounting_reports/odoopi_accounting_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoopi_accounting_reports/odoopi_accounting_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoopi_accounting_reports.listing', {
#             'root': '/odoopi_accounting_reports/odoopi_accounting_reports',
#             'objects': http.request.env['odoopi_accounting_reports.odoopi_accounting_reports'].search([]),
#         })

#     @http.route('/odoopi_accounting_reports/odoopi_accounting_reports/objects/<model("odoopi_accounting_reports.odoopi_accounting_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoopi_accounting_reports.object', {
#             'object': obj
#         })
