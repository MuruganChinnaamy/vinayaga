# -*- coding: utf-8 -*-

{
    'name': "Employee sales order",
    'author': 'CMSTech',
    'category': 'Human Resources',
    'summary': """Display the number of quotations and sales order quickly on the Employee""",
    'license': 'AGPL-3',
    'website': 'http://www.cms.com',
    'description': """
""",
    'version': '11.0.1.0.0',
    'depends': ['hr','sale'],
    'data': ['security/employee_sales_order_security.xml','views/employee_view.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
