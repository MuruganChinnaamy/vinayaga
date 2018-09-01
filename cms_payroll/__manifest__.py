# -*- coding: utf-8 -*-
{
    'name': 'CMS Payroll Mgmt',
    'version': '11.0.2.4.0',
    'license': 'LGPL-3',
    'category': 'CMS Payroll',
    "sequence": 1,
    'summary': 'Manage Educational Fees',
    'complexity': "easy",
    'description': """
        Description    ======
    """,
    'author': 'CMS Tech',
    'website': 'http://www.cmstech.com',
    'depends': ['hr','hr_payroll','hr_contract','hr_payroll_account','cms_alw_ded','cms_payslip_mail'], 
    'data': [
        #'data/hr_holidays_data.xml',
#         'security/security.xml',
#         'security/ir.model.access.csv',
        
        'report/payslip_report.xml',
        #'views/hr_payslip_view.xml',
    ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
