# -*- coding: utf-8 -*-
from openerp import fields, models, api, _
from openerp import SUPERUSER_ID
from openerp.exceptions import ValidationError
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
import re

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    type = fields.Selection([
        ('consu', _('Consumable')),
        ('service', _('Service')),
        ('product', _('Stockable Product'))], string='Product Type', default='product', required=True,
        help='A stockable product is a product for which you manage stock. The "Inventory" app has to be installed.\n'
             'A consumable product, on the other hand, is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.\n'
             'A digital content is a non-material product you sell online. The files attached to the products are the one that are sold on '
             'the e-commerce such as e-books, music, pictures,... The "Digital Product" module has to be installed.')