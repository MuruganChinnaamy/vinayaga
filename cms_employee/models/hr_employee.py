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
    
    
    
    
    employee_id = fields.Char(
        'Employee ID', size=16, copy=False)
        
    employee_type = fields.Selection([
        ('farmer', 'Farmer'),
        ('labour', 'Labour'),
        ('employee', 'Employee'),
    ], string='Employee Type', default='farmer')
    branch_id = fields.Many2one('res.company', 'Branch')
    village_id = fields.Many2one('village.master', 'Village')
    field_officers = fields.Many2many('hr.employee','employee_id_id','farmer_id','employee_employee_farmers_rel','Field Officers')
    partner_id = fields.Many2one('res.partner', 'Partner')
    field_manager = fields.Boolean('Is a Field Manager')
    
    @api.multi
    def onchange_employee_type(self):
        for record in self:
            if record.employee_type == 'farmer':
                record.employee_id = self.env['ir.sequence'].next_by_code('cms.farmer.new')
            elif record.employee_type == 'labour':
                record.employee_id = self.env['ir.sequence'].next_by_code('cms.labour.new')
            else:
                record.employee_id = self.env['ir.sequence'].next_by_code('cms.employee.new')
                
    @api.multi
    def partner_create(self):
        for record in self:
            partner = self.env['res.partner'].create({
                                            'company_type':'person',
                                            'employee_id':record.id,
                                            'employee_type':record.employee_type,
                                            'name':record.name,
                                            'image':record.image,
                                            'company_id':record.branch_id.id
                                            })
            return partner
        
                
    @api.model
    def create(self,vals):
        res = super(HrEmployee, self).create(vals)
        res.onchange_employee_type()
        vals['employee_id'] = res.employee_id
        partner = res.partner_create()
        vals['partner_id'] = partner.id
        return res  
    
    
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    employee_id = fields.Many2one('hr.employee', 'Employee')
    employee_type = fields.Selection([
        ('farmer', 'Farmer'),
        ('labour', 'Labour'),
        ('employee', 'Employee')], string='Employee Type')
    
    
    





