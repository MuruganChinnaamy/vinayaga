# -*- coding: utf-8 -*-
{
    'name': 'CMS Payslip Mail',
    'version': '11.0.2.4.0',
    'license': 'LGPL-3',
    'category': 'CMS',
    "sequence": 1,
    'summary': 'Manage Pappaya Payslip Mail',
    'complexity': "easy",
    'description': """
        Description    ======
    """,
    'author': 'CMS Tech',
    'website': 'http://www.cmstech.com',
    'depends': ['hr','hr_payroll'], 
    'data': [
        
        'data/mail_template_data_payslip.xml',
    ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
