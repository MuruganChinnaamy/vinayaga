# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
from odoo import tools, _
from odoo.exceptions import UserError, AccessError, ValidationError
import re
import calendar

class other_allowance_and_deduction(models.Model):
    _name='other.allowance.and.deduction'
    _description='Other Allowance and Deduction'
    
    name = fields.Char('Description', required=True, readonly=True, states={'draft': [('readonly', False)]})
    date_from = fields.Date('Date From', required=True, readonly=True, states={'draft': [('readonly', False)]})
    date_to = fields.Date('Date To', required=True, readonly=True, states={'draft': [('readonly', False)]})
    salary_rule_id = fields.Many2one('hr.salary.rule', 'Salary Rule', required=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'), ('done','Done'),('archived','Archived')], 'State', default='draft', readonly=True)
    other_allowance_and_deduction_line = fields.One2many('other.allowance.and.dedution.line', 'other_allowance_and_deduction_id', 'Allowance and Deduction Lines', required=True, readonly=True, states={'draft': [('readonly', False)]})
    other_allowance_and_deduction_log = fields.One2many('other.allowance.and.deduction.log', 'other_allowance_and_deduction_id', 'Change Log', readonly=True)
    allowance_or_deduction = fields.Selection([('allowance', 'Allowance'), ('deduction', 'Deduction')])
    
    _sql_constraints = [
        ('date_from_date_to_salary_rule_id_unique', 'unique (date_from, date_to, salary_rule_id)', 'Duplicate - Same Allowance repeated for given date range !'),
    ]
    
#     @api.onchange('salary_rule_id')
#     def onchange_salary_rule_id(self):
#         if self.salary_rule_id and self.salary_rule_id.category_id and self.salary_rule_id.category_id.code == 'ENCASH':
#             self.allowance_or_deduction = 'allowance'
#         elif self.salary_rule_id and self.salary_rule_id.category_id and self.salary_rule_id.category_id.code == 'DED':
#             self.allowance_or_deduction = 'deduction'
    
    @api.model
    def default_get(self, fields):
        res = super(other_allowance_and_deduction, self).default_get(fields)
        
        res['date_from'] = datetime.strftime(datetime.today(), "%Y-%m-01")
        res['date_to'] = datetime.strftime(datetime.today()+relativedelta(months=+1, day=1, days=-1), "%Y-%m-%d")
        
        return res

    @api.multi
    def button_confirm(self):
        for record in self:
            for line in record.other_allowance_and_deduction_line:
                line.write({'state': 'done'})
            other_allowance_and_deduction_log = [(0, 0, {
                'state_from': 'draft',
                'state_to': 'done',
                'user_id': record._uid,
                'activity_time': datetime.now()
                })]
            record.write({'other_allowance_and_deduction_log': other_allowance_and_deduction_log, 'state': 'done'})
    
    @api.multi
    def button_reset(self):
        for record in self:
            for line in record.other_allowance_and_deduction_line:
                line.write({'state': 'draft'})
            other_allowance_and_deduction_log = [(0, 0, {
                'state_from': record.state,
                'state_to': 'draft',
                'user_id': record._uid,
                'activity_time': datetime.now()
                })]
            record.write({'other_allowance_and_deduction_log': other_allowance_and_deduction_log, 'state': 'draft'})    
    
    @api.multi
    def button_archive(self):
        for record in self:
            for line in record.other_allowance_and_deduction_line:
                line.write({'state': 'archived'})
            other_allowance_and_deduction_log = [(0, 0, {
                'state_from': record.state,
                'state_to': 'archived',
                'user_id': record._uid,
                'activity_time': datetime.now()
                })]
            record.write({'other_allowance_and_deduction_log': other_allowance_and_deduction_log, 'state': 'archived'})    

class other_allowance_and_deduction_line(models.Model):
    _name='other.allowance.and.dedution.line'
    
    other_allowance_and_deduction_id = fields.Many2one('other.allowance.and.deduction', 'Other Allowance and Deduction ID')
    employee_id = fields.Many2one('hr.employee', 'Employee', readonly=True, states={'draft': [('readonly', False)]})
    amount = fields.Float('Amount', required=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'), ('done','Done'),('archived','Archived')], 'State', default='draft', readonly=True)
    description = fields.Char('Remarks', readonly=True, states={'draft': [('readonly', False)]})

    _sql_constraints = [
        ('employee_id_other_allowance_and_deduction_id_unique', 'unique (employee_id, other_allowance_and_deduction_id)', 'Duplicate - Same Employee repeated !'),
    ]
    
class other_allowance_and_deduction_log(models.Model):
    _name='other.allowance.and.deduction.log'
    
    user_id = fields.Many2one('res.users', 'User', readonly=True)
    activity_time = fields.Datetime('Changed On', readonly=True)
    state_from = fields.Selection([('draft', 'Draft'), ('done','Done'),('archived','Archived')], readonly=True)
    state_to = fields.Selection([('draft', 'Draft'), ('done','Done'),('archived','Archived')], readonly=True)
    other_allowance_and_deduction_id = fields.Many2one('other.allowance.and.deduction', 'Other Allowance and Deduction ID', readonly=True)
    
