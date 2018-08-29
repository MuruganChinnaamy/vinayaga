# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import re
from datetime import date, timedelta as td

class ResCompany(models.Model):
    _inherit = "res.company"
    _order = "id asc"
    
#     banker_code = fields.Char(string="Banker Code")
#     wpf_type = fields.Char(string="WPF Type")
#     wps_type = fields.Char(string="WPS Type")
#     sal_control_record = fields.Char(string="Salary Account Record")
#     emp_bic = fields.Char(string="Employee Banker Code    ")
    
    
    @api.one
    def copy(self, default=None):
        raise ValidationError('You are not allowed to Duplicate')
    
   
    
    def _validate_name(self, name):
        if name:
            if not re.match('^[a-zA-Z\d\s]*$', name):
                raise ValidationError('Please enter a valid Name.')
            return True
        else:
            return False
    
    def validate_zip(self, zip_code):
        if zip_code:
            match_zip_code = re.match('^[\d]*$', zip_code)
            if not match_zip_code or len(zip_code) != 6:
                raise ValidationError("Please enter a valid 6 digit zip code.")
            return True
        else:
            return False
    
    def validate_phone(self, phone_no):
        if phone_no:
            match_phone_no = re.match('^[\d]*$', phone_no)
            if not match_phone_no:
                raise ValidationError('Please enter a valid phone number.')
            return True
        else:
            return False
    
    def validate_mobile(self, mobile):
        if mobile:
            match_mobile = re.match('^[\d]*$', mobile)
            if not match_mobile or len(mobile) != 10:
                raise ValidationError('Please enter a valid 10 digit mobile number.')
            return True
        else:
            return False
        
    def validate_email(self, email):
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
        else:
            raise ValidationError('Please enter a valid E-mail Address.')
    
    
    @api.onchange('phone')
    def _onchange_phone(self):
        if self.phone:
            self.validate_phone(self.phone)
#             if self.type == 'school':
#                 return {'domain': {'parent_id': [('type', 'in', ['corporate', 'society']),('id', '!=', self.search([('parent_company','=',True)]).id)]}}
    
    
    @api.onchange('mobile')
    def _onchange_mobile(self):
        if self.mobile:
            self.validate_mobile(self.mobile)
    
    @api.onchange('email')
    def _onchange_email(self):
        if self.email:
            if self.search([('email','=',self.email)]).id:
                raise ValidationError("The given Email Address already exists.")
            self.validate_email(self.email)
            
    @api.onchange('zip')
    def _onchange_zip(self):
        if self.zip:
            self.validate_zip(self.zip)        
    
    def _validate_vals(self, vals):
        if 'email' in vals.keys() and vals.get('email'):
            if self.search([('email','=', vals.get('email'))]).id:
                raise ValidationError("The given Email Address already exists.")
            self.validate_email(vals.get('email'))
        if 'phone' in vals.keys() and vals.get('phone'):
            self.validate_phone(vals.get('phone'))
        if 'mobile' in vals.keys() and vals.get('mobile'):
            self.validate_mobile(vals.get('mobile'))
        if 'zip' in vals.keys() and vals.get('zip'):
            self.validate_zip(vals.get('zip'))
        return True
    
    @api.model
    def create(self, vals):
        self._validate_vals(vals)
        res = super(ResCompany, self).create(vals)
        return res

    @api.multi
    def write(self, vals):
        self._validate_vals(vals)
        return super(ResCompany, self).write(vals)
    
    ''' Purpose: Restricting users to not to delete 'cms company' record. '''
    @api.multi
    def unlink(self):
        for company in self:
            if company.parent_company:
                raise Warning(_("This record is considered as master record.\nYou are not allowed to delete it."))
        return super(ResCompany, self).unlink()

#     @api.multi
#     @api.depends('name', 'type', 'code')
#     def name_get(self):
#         result = []
#         for company in self:
#             if company.name and company.code and company.type:
#                 name = str(company.code)+ ' ' + str(company.name) + ' ' + str(company.type).title()
#             else:
#                 name = company.name
#             result.append((company.id, name))
#         return result

