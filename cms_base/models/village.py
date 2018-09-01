# -*- coding: utf-8 -*-
from openerp import fields, models, api, _
from openerp import SUPERUSER_ID
from openerp.exceptions import ValidationError
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
import re

class VillageMaster(models.Model):
    _name = "village.master"
    
    name = fields.Char(string='Name', required=True)
    company_id = fields.Many2one('res.company',string="Branch")
    field_officers = fields.Many2many('hr.employee','employee_id','village_id','employee_village_rel','Field Officers')
    description = fields.Char(string='Description')
    
   