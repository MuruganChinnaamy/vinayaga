# -*- coding: utf-8 -*-
###################################################################################
#    A part of Open HRMS Project <https://www.cmstech.com>

#
###################################################################################
{
    'name': 'Employee Master',
    'version': '11.0.2.0.0',
    'summary': """Adding Advanced Fields In Employee Master""",
    'description': 'This module helps you to add more information in employee records.',
    'category': 'Generic Modules/Human Resources',
    'author': 'CMS Tech',
    'company': 'CMS Tech',
    'website': "https://www.cmstech.com",
    'depends': ['base', 'hr', 'mail','hr_contract','cms_base'],
    'data': [
        'views/hr_employee_view.xml',
    ],
    'demo': [],
#     'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
