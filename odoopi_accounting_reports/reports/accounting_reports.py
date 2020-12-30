import logging
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class TaqdeerAccountingTrailBalance(models.AbstractModel):
    _name = 'report.odoopi_accounting_reports.trail_balance_template_id'
    _description = 'Commission Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        account_ids = []
        accounts = []
        totals = {}
        period = {}
        period.update(date_from=data['date_from'])
        period.update(date_to=data['date_to'])

        if not data['account_ids']:
            accounts = accounts + self.env['account.account'].search([]).mapped('id')
        else:
            accounts = accounts + data['account_ids']
        for rec in accounts:
            account_move_line_1 = self.env['account.move.line'].search(
                [('date', 'in', [data['date_from']]), ('account_id', 'in', [rec])])
            account_move_line_2 = self.env['account.move.line'].search(
                [('date', '>', data['date_from']), ('date', '<=', data['date_to']), ('account_id', 'in', [rec])])
            # print('move -------------------1', len(account_move_line_1))
            # print('move -------------------2', len(account_move_line_2))
            debit_first = sum(account_move_line_1.mapped('debit'))
            credit_first = sum(account_move_line_1.mapped('credit'))
            debit_moves = sum(account_move_line_2.mapped('debit'))
            credit_moves = sum(account_move_line_2.mapped('credit'))
            debit_sum = debit_first + debit_moves
            credit_sum = credit_first + credit_moves
            debit_result = 0.00
            credit_result = 0.00
            if debit_sum > credit_sum:
                debit_result = debit_sum - credit_sum
                credit_result = 0.00
            if credit_sum > debit_sum:
                credit_result = credit_sum - debit_sum
                debit_result = 0.00
            if sum(account_move_line_2.mapped('balance')) != 0.00:
                account_ids.append({
                    'name': self.env['account.account'].browse(rec).name,
                    'code': self.env['account.account'].browse(rec).code,
                    'debit_first': round(debit_first, 2),
                    'credit_first': round(credit_first, 2),
                    'debit_moves': round(debit_moves, 2),
                    'credit_moves': round(credit_moves, 2),
                    'debit_result': round(debit_result, 2),
                    'credit_result': round(credit_result, 2),
                })
            totals.update(total_debit_first=sum(item['debit_first'] for item in account_ids))
            totals.update(total_credit_first=sum(item['credit_first'] for item in account_ids))
            totals.update(total_debit_moves=sum(item['credit_moves'] for item in account_ids))
            totals.update(total_credit_moves=sum(item['credit_moves'] for item in account_ids))
            totals.update(total_debit_result=sum(item['debit_result'] for item in account_ids))
            totals.update(total_credit_result=sum(item['credit_result'] for item in account_ids))
        report = report_obj._get_report_from_name('odoopi_accounting_reports.trail_balance_accounting_define_report_id')
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': account_ids,
            'totals': totals,
            'period': period,
        }


class AccountingXlsx(models.AbstractModel):
    _name = "report.odoopi_accounting_reports.accounting_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Partner XLSX Report"

    def generate_xlsx_report(self, workbook, data, docs):
        top_heading = ['First Period', 'Moves In Year', 'Balance']
        heading = ['Code', 'Account', 'Debit', 'Credit', 'Debit', 'Credit', 'Debit', 'Credit', ]
        heading_ref = ['Account', 'Debit', 'Credit', 'Description', '', 'Date']
        # workbook = xlsxwriter.Workbook(str(data['date_from']) + str(data['date_to']))
        account_ids = []
        accounts = []
        totals = {}
        period = {}
        period.update(date_from=data['date_from'])
        period.update(date_to=data['date_to'])
        sheet = workbook.add_worksheet(data['date_from'])
        cell_col_format = workbook.add_format()
        cell_col_format.set_fg_color('#ffffff')
        sheet2 = workbook.add_worksheet(str(data['date_from']) + _('By details '))
        cell_format = workbook.add_format({'bold': True, 'align': 'center'})
        x = 5
        y = 1
        z = 6
        row_num_1 = 0
        count = 1
        if not data['account_ids']:
            accounts = accounts + self.env['account.account'].search([]).mapped('id')
        else:
            accounts = accounts + data['account_ids']
        sheet2.set_column('B:G', 30, cell_col_format)
        sheet2.write_row('B' + str(x), heading_ref, cell_format)

        for sheet_2 in accounts:
            name_account = self.env['account.account'].browse(sheet_2).name + '/'
            name_account += self.env['account.account'].browse(sheet_2).code
            if name_account:
                account_moves = self.env['account.move.line'].search(
                    [('date', '>', data['date_from']), ('date', '<=', data['date_to']),
                     ('account_id', 'in', [sheet_2])])
                if account_moves:
                    sheet2.write(x + row_num_1, 0 + y, name_account, workbook.add_format(
                        {'bold': True, 'font_size': 10, 'align': 'center', 'bg_color': '#ffffff'}))
                    for index, moves in enumerate(account_moves):
                        # print(x + index + 1, index)
                        sheet2.write(x + row_num_1 + index + 1, y + 1, moves.debit,
                                     workbook.add_format({'align': 'center', 'bg_color': '#DCDCDC'}))
                        sheet2.write(x + row_num_1 + index + 1, y + 2, moves.credit,
                                     workbook.add_format({'align': 'center', 'bg_color': '#DCDCDC'}))
                        sheet2.write(x + row_num_1 + index + 1, y + 3, moves.name,
                                     workbook.add_format({'align': 'center', 'bg_color': '#DCDCDC'}))
                        sheet2.write(x + row_num_1 + index + 1, y + 4, moves.ref,
                                     workbook.add_format({'align': 'center', 'bg_color': '#DCDCDC'}))
                        sheet2.write(x + row_num_1 + index + 1, y + 5, moves.date, workbook.add_format(
                            {'num_format': 'mm/dd/yy', 'align': 'center', 'bg_color': '#DCDCDC'}))
                    count += len(account_moves) + 1
            row_num_1 = count
        for sheet_1 in accounts:

            #  -----------------------------------------------------------
            account_move_line_1 = self.env['account.move.line'].search(
                [('date', 'in', [data['date_from']]), ('account_id', 'in', [sheet_1])])
            account_move_line_2 = self.env['account.move.line'].search(
                [('date', '>', data['date_from']), ('date', '<=', data['date_to']), ('account_id', 'in', [sheet_1])])
            debit_first = sum(account_move_line_1.mapped('debit'))
            credit_first = sum(account_move_line_1.mapped('credit'))
            debit_moves = sum(account_move_line_2.mapped('debit'))
            credit_moves = sum(account_move_line_2.mapped('credit'))
            debit_sum = debit_first + debit_moves
            credit_sum = credit_first + credit_moves
            debit_result = 0.00
            credit_result = 0.00
            if debit_sum > credit_sum:
                debit_result = debit_sum - credit_sum
                credit_result = 0.00
            if credit_sum > debit_sum:
                credit_result = credit_sum - debit_sum
                debit_result = 0.00
            if sum(account_move_line_2.mapped('balance')) != 0.00:
                account_ids.append({
                    'name': self.env['account.account'].browse(sheet_1).name,
                    'code': self.env['account.account'].browse(sheet_1).code,
                    'debit_first': round(debit_first, 2),
                    'credit_first': round(credit_first, 2),
                    'debit_moves': round(debit_moves, 2),
                    'credit_moves': round(credit_moves, 2),
                    'debit_result': round(debit_result, 2),
                    'credit_result': round(credit_result, 2),
                })
            totals.update(total_debit_first=sum(item['debit_first'] for item in account_ids))
            totals.update(total_credit_first=sum(item['credit_first'] for item in account_ids))
            totals.update(total_debit_moves=sum(item['credit_moves'] for item in account_ids))
            totals.update(total_credit_moves=sum(item['credit_moves'] for item in account_ids))
            totals.update(total_debit_result=sum(item['debit_result'] for item in account_ids))
            totals.update(total_credit_result=sum(item['credit_result'] for item in account_ids))
        sheet.write('D' + str(z), top_heading[0], cell_format)
        sheet.write('F' + str(z), top_heading[1], cell_format)
        sheet.write('H' + str(z), top_heading[2], cell_format)
        sheet.write_row('B' + str(x), heading, cell_format)

        sheet.set_column('B:I', 25, cell_col_format)
        for index, val in enumerate(account_ids):
            sheet.write('B' + str(x + index + 1), val['code'], cell_format)
            sheet.write('C' + str(x + index + 1), val['name'], cell_format)
            sheet.write('D' + str(x + index + 1), val['debit_first'], cell_format)
            sheet.write('E' + str(x + index + 1), val['credit_first'], cell_format)
            sheet.write('F' + str(x + index + 1), val['debit_moves'], cell_format)
            sheet.write('G' + str(x + index + 1), val['credit_moves'], cell_format)
            sheet.write('H' + str(x + index + 1), val['debit_result'], cell_format)
            sheet.write('I' + str(x + index + 1), val['credit_result'], cell_format)
        # sheet.write('B' + str(6 + val), totals['total_debit_first'])
