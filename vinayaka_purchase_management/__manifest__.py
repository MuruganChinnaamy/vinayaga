# -*- coding: utf-8 -*-

{
    'name': 'Vinayaka Purchase Management',
    'version': '1.0',
    'category': 'Purchases',
    'sequence': 60,
    'summary': 'Purchase Orders, Receipts, Vendor Bills',
    'description': "",
    'website': 'https://www.odoo.com/page/purchase',
    'depends': ['stock_account','purchase'],
    'data': [
        'views/vinayaka_purchase_view.xml',
    ],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
