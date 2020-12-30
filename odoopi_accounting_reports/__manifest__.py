# -*- coding: utf-8 -*-
{
    'name': "odoopi Accounting Reports",

    'summary': """
    Accounting reports pdf Excel
    """,

    'description': """
        
    """,

    'author': "Abdalmola Mustafa",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'report_xlsx', 'accounting_pdf_reports'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/accounting.xml',
        'reports/accounting.xml',
        'views/templates.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
