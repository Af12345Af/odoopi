# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


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
