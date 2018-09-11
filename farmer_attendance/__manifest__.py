# -*- coding: utf-8 -*-
{
    'name': 'Former Attendance',
    'version': '11.0.2.4.0',
    'license': 'LGPL-3',
    'category': 'ERP',
    "sequence": -1,
    'summary': 'Manage former bill',
    'complexity': "easy",
    'description': """
        Description    ======
    """,
    'author': 'Murugan',
    'website': 'http://www.cmshitech.com',
    'depends': ['cms_base','sale','purchase','web'],
    'data': [
        
        'views/daily_attendance_view.xml',
        'views/web.xml',
        
    ],
    "qweb": ["static/src/xml/web.xml"],
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/icon.png'],
}
