# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
from odoo import tools, _
from odoo.exceptions import UserError, AccessError, ValidationError
import re
import calendar


class HrPayslipRun(models.Model):
    _inherit='hr.payslip.run'
    
    @api.multi
    def send_email_bulk(self):
        for record in self:
            for payslip in record.slip_ids:
                template_obj = self.env['mail.template']
                ir_model_data = self.env['ir.model.data']
                template_id = ir_model_data.get_object_reference('pappaya_payslip_mail', 'email_template_edi_payslip')[1]
                if template_id:
                    if payslip.employee_id.user_id.partner_id and payslip.state == 'done':
                        if payslip.employee_id.id:
                            template_obj.browse(template_id).send_mail(payslip.id, force_send=True)
        return True
    
    

class HrPayslip(models.Model):
    _inherit='hr.payslip'
    _description='Hr Payslip Send via mail'
    
    

#          #  Set/Modify the values for the template.
#             values['subject'] = subject you want to show
#             values['email_to'] = receiver of the email
#             values['partner_to'] = partner ids
#             values['body'] = body_html
#               .....
#               .....
#         #--------------------------------------------------------------
#         #----------------if template id is not created-----------------
#             values = {
#                         'subject': 'subect ',
#                         'body_html': 'Message to be sent',
#                         'email_to': receiver email,
#                         'email_from': 'sender_email',
#                         values['partner_to'] : partner ids
#                         }
          #---------------------------------------------------------------
        
    
    @api.multi
    def action_payslip_send(self):
        '''
        This function opens a window to compose an email, with the edi payslip template message loaded by default
        '''
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('pappaya_payslip_mail', 'email_template_edi_payslip')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        update=ctx.update({
            'default_model': 'hr.payslip',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
