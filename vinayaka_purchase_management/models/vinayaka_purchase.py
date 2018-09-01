# -*- coding: utf-8 -*-

from odoo import api, fields, models

class res_partner(models.Model):
    _inherit='res.partner'
    
    is_farmer = fields.Boolean('Is Farmer')

    @api.mutli
    def create_supplier_location(self):
        for record in self:
            location_dict = {}
            ware_house_id = self.env['stock.warehouse'].search([('company_id','=',record.company_id)]).id or False
            location_dict.update({
                'name': record.name+' - Location',
                'usage':'internal',
                'warehouse_id': ware_house_id,
                'supplier_id': record.id,
                'is_farmer_location': True
                })
            return self.env['stock.location'].create(location_dict)
            