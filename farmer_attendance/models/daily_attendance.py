# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import re
from datetime import date, timedelta as td
import string

class DailyAttendance(models.Model):
    _name='daily.attendance'

    company_id = fields.Many2one('res.company', 'Branch')
    attendance_date = fields.Date(string='Attendance Date')
    area_id = fields.Char(string='Area')
    buying_supervisor = fields.Many2one('hr.employee',string="Buying Supervisor")
    buying_assistant = fields.Many2one('hr.employee', string="Buying Assistant")
    lines = fields.One2many('daily.attendance.line','attendance_id',string='Attendance Line')
    state = fields.Selection([('draft', 'Draft'),('done', 'Done')], default='draft')
    
    # vehicle Details
    vehicle_no = fields.Char(string='Vehicle No')
    opening_km = fields.Float(string='Opening K.M.')
    closing_km = fields.Float(string='Closing K.M.')
    
    # Total KG
    total_first_grade = fields.Float('First Grade KG',compute="_get_total_first_grade")
    total_second_grade = fields.Float('Second Grade KG',compute="_get_total_second_grade")
    total_third_grade = fields.Float('Third Grade KG',compute="_get_total_third_grade")
    total_fourth_grade = fields.Float('Fourth Grade KG',compute="_get_total_fourth_grade")
    total_fifth_grade = fields.Float('Fifth Grade KG',compute="_get_total_fifth_grade")
    total_six_grade = fields.Float('Six Grade KG',compute="_get_total_six_grade")
    total = fields.Float(string='Total',compute="_get_total_grade")
    
    
    @api.depends('lines')
    def _get_total_first_grade(self):
        for record in self:
            total = 0.00
            for line in record.lines:
                total += line.first_grade
            record.total_first_grade = total
    
    @api.depends('lines')
    def _get_total_second_grade(self):
        for record in self:
            total = 0.00
            for line in record.lines:
                total += line.second_grade
            record.total_second_grade = total
            
            
    @api.depends('lines')
    def _get_total_third_grade(self):
        for record in self:
            total = 0.00
            for line in record.lines:
                total += line.third_grade
            record.total_third_grade = total
            
            
    @api.depends('lines')
    def _get_total_fourth_grade(self):
        for record in self:
            total = 0.00
            for line in record.lines:
                total += line.fourth_grade
            record.total_fourth_grade = total
                
    
    @api.depends('lines')
    def _get_total_fifth_grade(self):
        for record in self:
            total = 0.00
            for line in record.lines:
                total += line.fifth_grade
            record.total_fifth_grade = total
            
    @api.depends('lines')
    def _get_total_six_grade(self):
        for record in self:
            total = 0.00
            for line in record.lines:
                total += line.six_grade
            record.total_six_grade = total        
    
    @api.depends('lines')        
    def _get_total_grade(self):
        for record in self:
            record.total = record.total_first_grade + record.total_second_grade + record.total_third_grade \
            + record.total_fourth_grade + record.total_fifth_grade + record.total_six_grade
        
    
    
    

DailyAttendance()

class DailyAttendanceLine(models.Model):
    _name="daily.attendance.line"
    
    attendance_id = fields.Many2one('daily.attendance',string='Daily Attendance')
    farmer_id = fields.Many2one('hr.employee',string='Farmer Name')
    village_id = fields.Char(string='Village Name')
    first_grade = fields.Float('First Grade KG')
    second_grade = fields.Float('Second Grade KG')
    third_grade = fields.Float('Third Grade KG')
    fourth_grade = fields.Float('Fourth Grade KG')
    fifth_grade = fields.Float('Fifth Grade KG')
    six_grade = fields.Float('Six Grade KG')
    total = fields.Float(string='Total', compute="_get_lines_total")
    
    @api.depends('first_grade','second_grade','third_grade','fourth_grade','fifth_grade','six_grade')
    def _get_lines_total(self):
        for record in self:
            record.total = record.first_grade + record.second_grade + record.third_grade \
            + record.fourth_grade + record.fifth_grade + record.six_grade
                            
    
    
    
    
DailyAttendanceLine()
    