# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import re
from datetime import date, timedelta as td

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
    total_first_grade = fields.Float('First Grade KG')
    total_second_grade = fields.Float('Second Grade KG')
    total_third_grade = fields.Float('Third Grade KG')
    total_fourth_grade = fields.Float('Fourth Grade KG')
    total_fifth_grade = fields.Float('Fifth Grade KG')
    total_six_grade = fields.Float('Six Grade KG')
    total = fields.Float('Total')
    
    

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
    total = fields.Float('Total')
    
    
    
    
DailyAttendanceLine()
    