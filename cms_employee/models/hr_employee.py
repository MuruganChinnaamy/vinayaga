# -*- coding: utf-8 -*-
###################################################################################
###################################################################################
from odoo import api, fields, models
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
from odoo import tools, _
from odoo.exceptions import UserError, AccessError, ValidationError
import re
import calendar


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    employee_id = fields.Char(string='Employee ID')
    employee_type = fields.Selection([
        ('farmer', 'Farmer'),
        ('labour', 'Labour'),
        ('employee', 'Employee'),
    ], string='Employee Type', default='farmer')
    branch_id = fields.Many2one('res.company', 'Branch')
    village_id = fields.Many2one('village.master', 'Village')
    field_officers = fields.Many2many('hr.employee','employee_id_id','farmer_id','employee_employee_farmers_rel','Field Officers')
    





