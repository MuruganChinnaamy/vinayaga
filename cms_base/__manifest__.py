# -*- coding: utf-8 -*-
{
    'name': 'CMS base',
    'version': '11.0.2.4.0',
    'license': 'LGPL-3',
    'category': 'ERP',
    "sequence": -1,
    'summary': 'Manage Form',
    'complexity': "easy",
    'description': """
        Description    ======
    """,
    'author': 'Think42Labs',
    'website': 'http://www.cmshitech.com',
    'depends': ['base'],
    'data': [
        
        'views/inherited_res_company_view.xml',
        'views/inherited_res_user_view.xml',
        'menu/menu.xml'
        
    ],
    'qweb': ['static/src/xml/help_template.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/icon.png'],
}
