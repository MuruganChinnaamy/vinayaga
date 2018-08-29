# -*- coding: utf-8 -*-
from openerp import fields, models, api, _
from openerp import SUPERUSER_ID
from openerp.exceptions import ValidationError
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
import re

class ResUsers(models.Model):
    _inherit = "res.users"
    _order = "id asc"
    
    # These two fields used for updating company_id in allowed companies based on user selection
#     school_id = fields.Many2one('res.company', 'School Name', required=1)
    super_admin = fields.Boolean('Super Admin')
    type = fields.Selection([('corporate','Corporate'), ('society','Society'), ('school','School')])
    
    phone = fields.Char('Phone', size=15)
    mobile = fields.Char(related='partner_id.mobile', inherited=True, size=10)
    phone_country_code = fields.Char()
    mobile_country_code = fields.Char()
    
    company_id = fields.Many2one('res.company', 'School Name', required=1)
    image = fields.Binary('Street', related='partner_id.image', inherited=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], default='male', required=True)
    birth_date = fields.Date('Date of Birth')
    street = fields.Char('Street', related='partner_id.street', inherited=True)
    street2 = fields.Char('Street2', related='partner_id.street2', inherited=True)
    zip = fields.Char('Zip', size=6, related='partner_id.zip', inherited=True)
    city =  fields.Char('City', related='partner_id.city', inherited=True)
    state_id = fields.Many2one("res.country.state", 'State', related='partner_id.state_id', inherited=True)
    country_id = fields.Many2one("res.country",'Country', related='partner_id.country_id', inherited=True)
    email = fields.Char(related='partner_id.email', inherited=True)
    #company_type = fields.Selection([('person', 'Staff'), ('company', 'School')], related='partner_id.company_type', inherited=True, string='User Type')
    middle_name = fields.Char('Middle Name')
    last_name = fields.Char('Last Name')
    date_of_joining = fields.Date('Date of Joining')
    # Access Right Groups
    # HR
#     pa_general_manager = fields.Boolean('General Manager')
#     pa_department_manager = fields.Boolean('Department Manager')
#     pa_manager = fields.Boolean('Manager')
#     pa_officer = fields.Boolean('Officer')
#     pa_employee = fields.Boolean('Employee')
#     # Purchase
#     purchase_user_level1 = fields.Boolean('Accountant')
#     purchase_user_level2 = fields.Boolean('Zonal Finance Officer')
#     purchase_user_level3 = fields.Boolean('Regional Finanace officer')
#     # Account
#     account_user_level1 = fields.Boolean('Accountant')
#     account_user_level2 = fields.Boolean('Zonal Finance Officer')
#     account_user_level3 = fields.Boolean('Regional Finanace officer')
#     account_user_level4 = fields.Boolean('Finance Officer')
    
    @api.one
    @api.constrains('email')
    def _check_unique_email(self):
        if self.email:
            if len(self.search([('email','=',self.email)])) > 1:
                raise ValidationError("Email already exists")
    
    
    @api.onchange('mobile')
    def _onchange_mobile(self):
        if self.mobile:
            self.validate_mobile(self.mobile)
            
    @api.onchange('phone')
    def _onchange_phone(self):
        if self.phone:
            self.validate_phone(self.phone)
    
    @api.onchange('email')
    def _onchange_email(self):
        if self.email:
            self.validate_email(self.email)
            if self.search([('email','=',self.email)]).id:
                raise ValidationError("The given Email Address already exists")
        
    @api.onchange('zip')
    def _onchange_zip(self):
        if self.zip:
            self.env['res.company'].validate_zip(self.zip)
    
    @api.multi
    @api.constrains('birth_date') 
    def check_date(self):
        if self.birth_date:
            if datetime.strptime(self.birth_date, DEFAULT_SERVER_DATE_FORMAT).date() >= datetime.now().date():
                raise ValidationError('Please check the entered Date of Birth')
     
    @api.multi
    @api.constrains('date_of_joining') 
    def check_date_of_joining(self):
        if self.date_of_joining:
            if datetime.strptime(self.date_of_joining, DEFAULT_SERVER_DATE_FORMAT).date() > datetime.now().date():
                raise ValidationError('Please enter a valid date of joining')
        
    def _validate_vals(self, vals):
        if 'email' in vals.keys() and vals.get('email'):
            if self.search([('email','=', vals.get('email'))]).id:
                raise ValidationError("The given Email Address already exists")
            self.validate_email(vals.get('email'))
        if 'mobile' in vals.keys() and vals.get('mobile'):
            self.validate_mobile(vals.get('mobile'))
        if 'phone' in vals.keys() and vals.get('phone'):
            self.validate_phone(vals.get('phone'))
        if 'zip' in vals.keys() and vals.get('zip'):
            self.validate_zip(vals.get('zip'))
        return True
    
    def _get_groups(self, existing_user_base_groups, groups):
        group_ids = existing_user_base_groups
        for g in groups:
            group = self.env.ref(g, raise_if_not_found=False)
            if group:
                group_ids.append(group.id)
        return [[6, False, group_ids]] 
    
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
    
    @api.model
    def create(self, vals):
        self._validate_vals(vals)
#         groups = []
#         if vals.get('purchase_user_level1'):
#             groups.append('purchase.group_purchase_user'); groups.append('pappaya_base.purchase_user_level1')            
#         if vals.get('purchase_user_level2'):
#             groups.append('purchase.group_purchase_manager'); groups.append('pappaya_base.purchase_user_level2')
#         if vals.get('purchase_user_level3'):
#             groups.append('purchase.group_purchase_manager'); groups.append('pappaya_base.purchase_user_level3')
#         # HR
#         if vals.get('pa_general_manager'):
#             groups.append('pappaya_hr_exit.group_genaral_manager_for_exit')
#         if vals.get('pa_department_manager'):
#             groups.append('pappaya_hr_exit.group_department_manager_for_exit')
#         if vals.get('pa_manager'):
#             groups.append('hr.group_hr_manager')
#         if vals.get('pa_officer'):
#             groups.append('hr.group_hr_user')
#         if vals.get('pa_employee'):
#             groups.append('base.group_user')
#         
#         # Account
#         if vals.get('account_user_level1'):
#             groups.append('account.group_account_invoice'); groups.append('pappaya_base.account_user_level1')
#         if vals.get('account_user_level2'):
#             groups.append('account.group_account_manager'); groups.append('pappaya_base.account_user_level2')
#         if vals.get('account_user_level3'):
#             groups.append('account.group_account_manager'); groups.append('pappaya_base.account_user_level3')
#         if vals.get('account_user_level4'):
#             groups.append('account.group_account_user'); groups.append('pappaya_base.account_user_level4')
#         
#         if groups:
#             vals.update({'groups_id' : self._get_groups([], groups)})
#         elif 'active' in vals and not groups:
#             raise ValidationError("Please select at least one 'User Role'.")
        
        return super(ResUsers, self).create(vals)
    
    @api.multi
    def write(self, vals):
        self._validate_vals(vals)
#         groups = [#
#                   'pappaya_base.purchase_user_level1', 'pappaya_base.purchase_user_level2', 'pappaya_base.purchase_user_level3',
#                   'purchase.group_purchase_user', 'purchase.group_purchase_manager',
#                   #
#                   'pappaya_hr_exit.group_genaral_manager_for_exit',
#                   'pappaya_hr_exit.group_department_manager_for_exit',
#                   'hr.group_hr_manager',
#                   'hr.group_hr_user',
#                   #
#                   'pappaya_base.account_user_level1', 'pappaya_base.account_user_level2', 'pappaya_base.account_user_level3', 'pappaya_base.account_user_level4',
#                   'account.group_account_invoice', 'account.group_account_manager', 'account.group_account_user'
#                 ]
#         # ***************************** Purchase Management *****************************
#         if 'purchase_user_level1' in vals and not vals.get('purchase_user_level1') or not self.purchase_user_level1:
#             if 'purchase.group_purchase_user' in groups:
#                 groups.remove('purchase.group_purchase_user'); 
#             if 'pappaya_base.purchase_user_level1' in groups:
#                 groups.remove('pappaya_base.purchase_user_level1')
#             if 'purchase_user_level1' in vals and vals.get('purchase_user_level1'):
#                 if 'purchase.group_purchase_user' not in groups:
#                     groups.append('purchase.group_purchase_user'); 
#                 if 'pappaya_base.purchase_user_level1' not in groups:
#                     groups.append('pappaya_base.purchase_user_level1')
#                 
#         if 'purchase_user_level2' in vals and not vals.get('purchase_user_level2') or not self.purchase_user_level2:
#             if 'purchase.group_purchase_manager' in groups:
#                 groups.remove('purchase.group_purchase_manager'); 
#             if 'pappaya_base.purchase_user_level2' in groups:
#                 groups.remove('pappaya_base.purchase_user_level2')
#             if 'purchase_user_level2' in vals and vals.get('purchase_user_level2'):
#                 if 'purchase.group_purchase_manager' not in groups:
#                     groups.append('purchase.group_purchase_manager')
#                 if 'pappaya_base.purchase_user_level2' not in groups:
#                     groups.append('pappaya_base.purchase_user_level2')
#                 
#         if 'purchase_user_level3' in vals and not vals.get('purchase_user_level3') or not self.purchase_user_level3:
#             if 'purchase.group_purchase_manager' in groups:
#                 groups.remove('purchase.group_purchase_manager')
#             if 'pappaya_base.purchase_user_level3' in groups:
#                 groups.remove('pappaya_base.purchase_user_level3')
#             if 'purchase_user_level3' in vals and vals.get('purchase_user_level3'):
#                 if 'purchase.group_purchase_manager' not in groups:
#                     groups.append('purchase.group_purchase_manager'); 
#                 if 'pappaya_base.purchase_user_level3' not in groups:
#                     groups.append('pappaya_base.purchase_user_level3')
#         # ***************************** HR Management *****************************
#         if 'pa_general_manager' in vals and not vals.get('pa_general_manager') or not self.pa_general_manager:
#             groups.remove('pappaya_hr_exit.group_genaral_manager_for_exit')
#             if 'pa_general_manager' in vals and vals.get('pa_general_manager'):
#                 groups.append('pappaya_hr_exit.group_genaral_manager_for_exit')
#         if 'pa_department_manager' in vals and not vals.get('pa_department_manager') or not self.pa_department_manager:
#             groups.remove('pappaya_hr_exit.group_department_manager_for_exit')
#             if 'pa_department_manager' in vals and vals.get('pa_department_manager'):
#                 groups.append('pappaya_hr_exit.group_department_manager_for_exit')
#         if 'pa_manager' in vals and not vals.get('pa_manager') or not self.pa_manager:
#             groups.remove('hr.group_hr_manager')
#             if 'pa_manager' in vals and vals.get('pa_manager'):
#                 groups.append('hr.group_hr_manager')
#         if 'pa_officer' in vals and not vals.get('pa_officer') or not self.pa_officer:
#             groups.remove('hr.group_hr_user')
#             if 'pa_officer' in vals and vals.get('pa_officer'):
#                 groups.append('hr.group_hr_user')
#         # ***************************** Accounting Management *****************************
#         if 'account_user_level1' in vals and not vals.get('account_user_level1') or not self.account_user_level1:
#             if 'account.group_account_invoice' in groups:
#                 groups.remove('account.group_account_invoice'); 
#             if 'pappaya_base.account_user_level1' in groups:
#                 groups.remove('pappaya_base.account_user_level1')
#             if 'account_user_level1' in vals and vals.get('account_user_level1'):
#                 if 'account.group_account_invoice' not in groups:
#                     groups.append('account.group_account_invoice')
#                 if 'pappaya_base.account_user_level1' not in groups:
#                     groups.append('pappaya_base.account_user_level1')
#         if 'account_user_level2' in vals and not vals.get('account_user_level2') or not self.account_user_level2:
#             if 'account.group_account_manager' in groups:
#                 groups.remove('account.group_account_manager')
#             if 'pappaya_base.account_user_level2' in groups:
#                 groups.remove('pappaya_base.account_user_level2')
#             if 'account_user_level2' in vals and vals.get('account_user_level2'):
#                 if 'account.group_account_manager' not in groups:
#                     groups.append('account.group_account_manager')
#                 if 'pappaya_base.account_user_level2' not in groups:
#                     groups.append('pappaya_base.account_user_level2')
#         if 'account_user_level3' in vals and not vals.get('account_user_level3') or not self.account_user_level3:
#             if 'account.group_account_manager' in groups:
#                 groups.remove('account.group_account_manager')
#             if 'pappaya_base.account_user_level3' in groups:
#                 groups.remove('pappaya_base.account_user_level3')
#             if 'account_user_level3' in vals and vals.get('account_user_level3'):
#                 if 'account.group_account_manager' not in groups:
#                     groups.append('account.group_account_manager')
#                 if 'pappaya_base.account_user_level3' not in groups:
#                     groups.append('pappaya_base.account_user_level3')
#         if 'account_user_level4' in vals and not vals.get('account_user_level4') or not self.account_user_level4:
#             if 'account.group_account_user' in groups:
#                 groups.remove('account.group_account_user')
#             if 'pappaya_base.account_user_level4' in groups:
#                 groups.remove('pappaya_base.account_user_level4')
#             if 'account_user_level4' in vals and vals.get('account_user_level4'):
#                 if 'account.group_account_user' not in groups:
#                     groups.append('account.group_account_user')
#                 if 'pappaya_base.account_user_level4' not in groups:
#                     groups.append('pappaya_base.account_user_level4')
#         # End        
#         print('groups :', groups)
#         if groups:
#             ir_module_category_ids = []; existing_base_groups = []
#             try:
#                 category_domain = ['Narayana Groups', 'Employees', 'Purchase Management', 'Accounting Groups', 'Purchases', 'Accounting & Finance']
#                 ir_module_category_ids = self.env['ir.module.category'].sudo().search([('name','in',category_domain)]).ids
#             except:
#                 pass
#             pappaya_groups = self.env['res.groups'].sudo().search([('category_id','in',ir_module_category_ids)]).ids
#             existing_user_groups = self.groups_id
#             for eug in existing_user_groups:
#                 if eug.id not in pappaya_groups and eug.id not in existing_base_groups:
#                     existing_base_groups.append(eug.id)
#             vals.update({'groups_id' : self._get_groups(existing_base_groups, groups)})
#              
        return super(ResUsers, self).write(vals)
    
    """ Purpose : Hiding 'Administrator' record in many2one fields. """
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if SUPERUSER_ID != self._uid:
            args += ([('id', '!=', 1)])
        mids = self.search(args)
        return mids.name_get()
    
    """ Purpose : Hiding 'Administrator' record when other user login and try to view in users menu if login user has access to view users menu. """
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if SUPERUSER_ID != self._uid:
            args += [('id', '!=', 1)]
        return super(ResUsers, self).search(args, offset, limit, order, count=count)

    ''' Purpose: Restricting every users to not to delete "Administrator" record '''
    @api.multi
    def unlink(self):
        for user in self:
            if user.id == 1 or user.id == user.id:
                raise ValidationError("Sorry, You are not allowed to delete it.\nThis record is considered as master configuration.")
        return super(ResUsers, self).unlink()
