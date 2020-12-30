# -*- coding: utf-8 -*-

from odoo import fields, models
from datetime import datetime, date


class AccountBalanceReport(models.TransientModel):
    _name = 'odoopi.account.balance'
    _description = 'Valuation Trail Balance'

    date_from = fields.Date(readonly=True, default=date(date.today().year - 1, 12, 31))
    date_to = fields.Date(default=date(date.today().year, 12, 31))
    account_ids = fields.Many2many('account.account')

    def print_trail_balance(self):
        data = {}
        for rec in self:
            if rec.date_from:
                data.update(date_from=rec.date_from)
            if rec.date_to:
                data.update(date_to=rec.date_to)
            if rec.account_ids:
                data.update(account_ids=rec.account_ids.mapped('id'))
            else:
                data.update(account_ids=[])

        return self.env.ref('odoopi_accounting_reports.trail_balance_accounting_define_report_id').report_action(self, data=data)

    def print_trail_balance_excel(self):
        data = {}
        for rec in self:
            if rec.date_from:
                data.update(date_from=rec.date_from)
            if rec.date_to:
                data.update(date_to=rec.date_to)
            if rec.account_ids:
                data.update(account_ids=rec.account_ids.mapped('id'))
            else:
                data.update(account_ids=[])

        return self.env.ref('odoopi_accounting_reports.accounting_xlsx').report_action([], data=data)
