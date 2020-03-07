# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date,datetime


class Methods(models.Model):
    _inherit = 'account.invoice'

    test = fields.Date()

    @api.multi
    def action_invoice_open(self):
        self._validate_date()
        return super(Methods, self).action_invoice_open()

    @api.multi
    def _validate_date(self):
        if self.number:
            self.test = date.today()

    @api.onchange('user_id')
    def _domain(self):
        user = self.env['res.users'].search([('login_date', '<=', datetime.today())])
        user_ids = []
        for val in user:
            user_ids.append(val.id)
        print(user_ids)
        # pass
        return {'domain': {'user_id': [('id', 'in', user_ids), ]}}
