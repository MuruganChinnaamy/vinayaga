# -*- coding: utf-8 -*-

from odoo import api, fields, models

class stock_location(models.Model):
    _inherit='stock.location'

    is_farmer_location = fields.Boolean('Is Farmer Location ?')
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse')
    

