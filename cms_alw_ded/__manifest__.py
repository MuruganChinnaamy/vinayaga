# -*- coding: utf-8 -*-
{
    'name': 'CMS Allowance and Deduction',
    'version': '11.0.2.4.0',
    'license': 'LGPL-3',
    'category': 'CMS',
    "sequence": 1,
    'summary': 'Manage Employee Allowance and Deduction',
    'complexity': "easy",
    'description': """
        Description    ======
    """,
    'author': 'CMS Tech',
    'website': 'http://www.cmstech.com',
    'depends': ['hr','hr_payroll'], 
    'data': [
        
        'views/allowance_and_deduction_view.xml',
    ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
