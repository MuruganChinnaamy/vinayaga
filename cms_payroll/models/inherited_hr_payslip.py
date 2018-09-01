# -*- coding:utf-8 -*-
import time
from datetime import datetime, timedelta
from datetime import time as datetime_time
from dateutil.relativedelta import relativedelta

import babel
import base64

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from num2words import num2words
from io import StringIO
from time import gmtime, strftime
import dateutil.parser

from xlwt import *
#from __builtin__ import True
try:
    import xlwt
except:
    raise osv.except_osv('Warning !','python-xlwt module missing. Please install it.')

import os

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    
            
    
    @api.multi
    def net_amount_in_words(self, key):
        net_amount = False
        net_amount_in_words = False
        for record in self:
            for line_id in record.line_ids:
                if line_id.category_id.code == 'NET':
                    net_amount = line_id.total
                    net_amount_in_words = 'Net Pay: '+num2words(line_id.total).title()+' IND only'
        if net_amount or net_amount_in_words:
            if key == 'net_amount':
                return net_amount
            elif key == 'net_amount_words':
                return net_amount_in_words
    
    @api.depends('lop_days','total_work_hours')
    def cal_paid_days_and_hours(self):
        for record in self:
            paid_days = 0.00
            paid_hours = 0.00
            record.paid_days = record.total_work_days - record.lop_days
            record.paid_hours = record.total_work_hours - record.lop_hours
            
    @api.depends('lop_hours','lop_days')
    def cal_lop_days_and_hours(self):
        for record in self:
            lop_days = 0.00
            lop_hours = 0.00
            for line in record.worked_days_line_ids:
                if line.code in ['PR','WF','PH','Leave']:
                    lop_days += line.number_of_days
                    lop_hours += line.number_of_hours
            record.lop_days = record.total_work_days - lop_days
            record.lop_hours = record.total_work_hours - lop_hours
                
    
    def _get_days_payable(self):
        working_days = 0.0
        for record_line in self.worked_days_line_ids:
            working_days += record_line.number_of_days
        return working_days
    
    @api.multi
    def work_days(self):
        unpaid = 0
        lst = []
        start = datetime.strptime(self.date_from, '%Y-%m-%d').date()
        end = datetime.strptime(self.date_to, '%Y-%m-%d').date()
        work_days = relativedelta(end,start)
        total_days = work_days.days + 1
        for rec in self.worked_days_line_ids:
            if rec.code == 'Unpaid':
                unpaid += rec.number_of_days
        vals = {}
        vals['total_days'] = total_days
        vals['paid_days'] = int(total_days - unpaid)
        lst.append(vals)
        return lst

    @api.multi
    def get_worked_day_lines_payslip(self):
        contracts, date_from, date_to = self.contract_id, self.date_from,self.date_to;
        print (self,"2222222222222222222222222222222222222222")
        """
        @param contract: Browse record of contracts
        @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
        """
        res = []
        # fill only if the contract as a working schedule linked
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            day_from = datetime.combine(fields.Date.from_string(date_from), datetime_time.min)
            day_to = datetime.combine(fields.Date.from_string(date_to), datetime_time.max)
            # leave Present
            print (type(date_to),"date_to")
            
            #date_from_time = date_from + ' 00:00:00'
            #date_to_time = date_to + ' 23:59:59'
            
            format_str = '%Y-%m-%d %H:%M:%S' # The format
#             datetime_from_obj = datetime.strptime(date_from_time, format_str)
#             datetime_to_obj = datetime.strptime(date_to_time, format_str)
#             print (type(datetime_from_obj),'datetime_from_obj')
            count = 0
            no_of_pr_hours = 0.00
            ot_of_pr_hours = 0.00
            no_of_weekly_days = 0
            
            # contracts configuration working hours and ot hours
            minimum_working_hr = self.contract_id.minimum_working_hr
            maxmum_working_hr = self.contract_id.maxmum_working_hr
            ot_hour_limit = self.contract_id.ot_hr_limit
            public_holiday_count = 0
            
            
            
            
            
            # weekly off fetch data
            weekly_days = []
            if self.contract_id.weekly_off:
                for weekly_line in self.contract_id.weekly_off.lines:
                    weekly_days.append(weekly_line.name)
            
            # holidays Calculation:
            holidays = self.env['yearly.holidays'].search([('state','=','done')])
            holidays_line = self.env['holidays.list'].search([('yearly_holidays_id','in',holidays.ids),('date','>=', date_from),('date','<=', date_to)])
            for public_holiday in holidays_line:
                holiday_puc = datetime.strptime(public_holiday.date, '%Y-%m-%d')
                if holiday_puc.weekday() not in weekly_days:
                    public_holiday_count += 1
            
            # date from to date to between dates checking
            dates_ranges= self.generate_dates(self.date_from,self.date_to)
            for current_date in dates_ranges:
                
                if current_date.weekday() not in weekly_days:
                    print (current_date,"current_datecurrent_date")
                    date_from_time = datetime.strftime(current_date,'%Y-%m-%d') + ' 00:00:00'
                    date_to_time = datetime.strftime(current_date,'%Y-%m-%d') + ' 23:59:59'
                    #date_from_time = datetime.strptime(date_from_str, format_str)
                    #date_to_time = datetime.strptime(date_to_str, format_str)
                    print (date_from_time,date_to_time,"date_to_timedate_to_timedate_to_time")
                    worked_hour = 0.00
                    for leaves in self.env['hr.attendance'].search([('employee_id', '=', self.employee_id.id),
                                                                    ('check_in','>=',date_from_time),
                                                                    ('check_out','<=', date_to_time)
                                                                    ]):
                        print (leaves,"lllllll")
                        worked_hour += leaves.worked_hours
                    if minimum_working_hr and maxmum_working_hr and minimum_working_hr <= worked_hour:
                        print ("AAAAAAAAAAAAA")
                        no_of_pr_hours += maxmum_working_hr
                    else:
                        print ("bbbbbbbbbbbbbb")
                        no_of_pr_hours += worked_hour
                    
                    if ot_hour_limit and worked_hour:
                        if maxmum_working_hr < worked_hour:
                            orgi_ot_hour_limit = maxmum_working_hr + ot_hour_limit
                            if orgi_ot_hour_limit < worked_hour:
                                ot_of_pr_hours += ot_hour_limit
                            else:
                                ot_of_pr_hours = worked_hour - maxmum_working_hr
                else:
                        no_of_weekly_days += 1 
             
            res.append({
                    'name': 'Present',
                    'sequence': 3,
                    'code': 'PR',
                    'number_of_days': no_of_pr_hours/maxmum_working_hr,
                    'number_of_hours': no_of_pr_hours,
                    'contract_id': contract.id,
                }
                )
            res.append({
                    'name': 'Over Time',
                    'sequence': 3,
                    'code': 'OT',
                    'number_of_days': ot_of_pr_hours/ maxmum_working_hr,
                    'number_of_hours': ot_of_pr_hours,
                    'contract_id': contract.id,
                    })
            
            res.append({
                    'name': 'Weekly Off',
                    'sequence': 3,
                    'code': 'WF',
                    'number_of_days': no_of_weekly_days,
                    'number_of_hours': no_of_weekly_days * maxmum_working_hr,
                    'contract_id': contract.id,
                    })
            res.append({
                    'name': 'Public Holiday',
                    'sequence': 3,
                    'code': 'PH',
                    'number_of_days': public_holiday_count,
                    'number_of_hours': public_holiday_count * maxmum_working_hr,
                    'contract_id': contract.id,
                    })
            
            
            # Leave absent
            count = 0
            total_leave_count = 0
            for holiday_status_id in self.env['hr.holidays.status'].sudo().search([('active','=',True)]):
                leave_count = 0
                for leaves in self.env['hr.holidays'].search([('employee_id', '=', self.employee_id.id),
                                                                   ('date_to', '<=', date_to),
                                                                   ('date_from','>=',date_from),
                                                                   ('type','=','remove'),
                                                                   ('state','=','validate'),
                                                                   ('holiday_status_id', '=', holiday_status_id.id)]):
                    leave_count += leaves.number_of_days_temp 
                    total_leave_count += leave_count
                # experince wise leave allowed monthly
                experince = self.employee_id.no_of_yrs
                status_line_conf = holiday_status_id.leave_configuration.search([('id','in', holiday_status_id.leave_configuration.ids),('years_service_from','<=',experince)])
                print  (status_line_conf,"status_line_conf")
                original_dict = {}
                for status_line in status_line_conf:
                    original_dict.update({
                                            status_line.years_service_to:status_line.per_month_days
                                            })
                print (original_dict,"original_dictoriginal_dict")
                
                max_key = None
                max_allow_days = 0
                if original_dict:
                    max_key = max(list(original_dict.keys()))
                    max_allow_days = original_dict[max_key]
                
                if leave_count and  holiday_status_id.name != 'LOP':    
                    if leave_count > max_allow_days: 
                        res.append({
                                'name': holiday_status_id.name,
                                'sequence': 4,
                                'code': 'Leave',
                                'number_of_days': (max_allow_days),
                                'number_of_hours': max_allow_days * 8,
                                'contract_id': contract.id,
                            }
                            )
                        # Leave Lop Leaves
                        res.append({
                                'name': holiday_status_id.name,
                                'sequence': 4,
                                'code': 'LOP',
                                'number_of_days': -(leave_count - max_allow_days),
                                'number_of_hours': (leave_count - max_allow_days) * 8,
                                'contract_id': contract.id,
                            }
                            )
                    else:
                        
                        res.append({
                                'name': holiday_status_id.name,
                                'sequence': 4,
                                'code': 'Leave',
                                'number_of_days': (leave_count),
                                'number_of_hours': leave_count * 8,
                                'contract_id': contract.id,
                            }
                            )
                        
                elif leave_count and  holiday_status_id.name == 'LOP':
                    res.append({
                            'name': holiday_status_id.name,
                            'sequence': 4,
                            'code': 'LOP',
                            'number_of_days': -(leave_count),
                            'number_of_hours': leave_count * 8,
                            'contract_id': contract.id,
                        }
                        )
            
            self.worked_days_line_ids = res
            
            input_lines = []
            leave_encashment = self.env['leave.encashment.request'].search([('requested_by','=',self.employee_id.id),('requested_date','>=',date_from),('requested_date','<=',date_to),('state','=','approved')])
            if leave_encashment:
                for leave_encash in leave_encashment:
                    input_lines.append((0,0,{
                                'name': leave_encash.name,
                                'sequence': 10,
                                'code': 'LE',
                                'amount':leave_encash.encashment_amount,
                                'contract_id': contract.id,
                            }
                            ))
                    leave_encash.write({'state':'paid'})
             # other allowance and deduction
            alw_ded_search = self.env['other.allowance.and.deduction'].search([('date_from','>=',date_from),('date_to','<=', date_to),('state','=','done')])
            employee_alw_ded = self.env['other.allowance.and.dedution.line'].search([('employee_id','=',self.employee_id.id),('other_allowance_and_deduction_id','in',alw_ded_search.ids)])
            for emp_alw_ded in employee_alw_ded:
                input_lines.append((0,0,{
                                'name': emp_alw_ded.other_allowance_and_deduction_id.salary_rule_id.name,
                                'sequence': 10,
                                'code': emp_alw_ded.other_allowance_and_deduction_id.salary_rule_id.code,
                                'amount':emp_alw_ded.amount,
                                'contract_id': contract.id,
                            }
                            ))
                emp_alw_ded.write({'state':'archived'})
            alw_ded_search.write({'state':'archived'})
            self.input_line_ids =  input_lines   
                
            # compute worked days
            #work_data = contract.employee_id.get_work_days_data(day_from, day_to, calendar=contract.resource_calendar_id)
            
    @api.depends('total_work_days','total_work_hours')
    def cal_total_days_and_hours(self):
        date_from = datetime.strptime(self.date_from, "%Y-%m-%d") 
        date_to = datetime.strptime(self.date_to, "%Y-%m-%d")        
        days_total = (date_to.date() - date_from.date()).days + 1
        print (days_total,"days_total")
        self.total_work_days = days_total
        self.total_work_hours = (days_total * 8)
            
            #
            
            
            
    @api.multi
    def generate_dates(self, date_from, date_to):
        dates = []
        td = timedelta(hours=24)
        current_date = datetime.strptime(date_from, "%Y-%m-%d").date()
        while current_date <= datetime.strptime(date_to, "%Y-%m-%d").date():
            dates.append(current_date)
            current_date += td
        return dates
    
    
class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'
    _description = 'Generate payslips for all selected employees'


    @api.multi
    def compute_sheet(self):
        print (self,"11111111111111111111111")
        payslips = self.env['hr.payslip']
        
        active_id = self.env.context.get('active_id')
        if active_id:
            [run_data] = self.env['hr.payslip.run'].browse(active_id).read(['date_start', 'date_end', 'credit_note','company_id'])
        from_date = run_data.get('date_start')
        to_date = run_data.get('date_end')
        company_id = run_data.get('company_id')
        print (company_id,"company_idcompany_idcompany_id")
        employee_ids = self.env['hr.employee'].search([('company_id','=', company_id[0]),('active','!=',False),('id','!=',1)]).ids
        self.employee_ids = employee_ids
        [data] = self.read()
        if not data['employee_ids']:
            raise UserError(_("You must select employee(s) to generate payslip(s)."))
        for employee in self.env['hr.employee'].browse(data['employee_ids']):
            slip_data = self.env['hr.payslip'].onchange_employee_id(from_date, to_date, employee.id, contract_id=False)
            res = {
                'employee_id': employee.id,
                'name': slip_data['value'].get('name'),
                'struct_id': slip_data['value'].get('struct_id'),
                'contract_id': slip_data['value'].get('contract_id'),
                'payslip_run_id': active_id,
                'input_line_ids': [(0, 0, x) for x in slip_data['value'].get('input_line_ids')],
                'worked_days_line_ids': [(0, 0, x) for x in slip_data['value'].get('worked_days_line_ids')],
                'date_from': from_date,
                'date_to': to_date,
                'credit_note': run_data.get('credit_note'),
                'company_id': employee.company_id.id,
            }
            payslips += self.env['hr.payslip'].create(res)
        for slip in payslips:
            #slip.worked_days_line_ids = None
            #slip.get_worked_day_lines_payslip()
            slip.compute_sheet()
            
           
            
            #for line in slip.line_ids:
                
                
        return {'type': 'ir.actions.act_window_close'}
    
    
    
class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
    _description = 'Payslip Batches'
    
    company_id = fields.Many2one('res.company','Company Name')
    
    
    @api.multi
    def generate_report_action(self):  
        for record in self:
            cwd = os.path.abspath(__file__)
            path = cwd.rsplit('/', 2)
            file_path = path[0] + '/data/po_label.txt'
            print (file_path,"44444444444")
            #sum_id = self.browse(cr,uid,ids[0])        
            #emp_ids=self._context['active_ids']
            n_edr=0
            tot_sal=0
    
            png_file = open(file_path, 'wb+')
            data11=''
            for ac_ids in self.slip_ids:
                no_of_days=0
                fixed_sal=0
                ded_sal = 0
                leave_days=0
                l_days=0
                var_sal=0
                sign_in_days=0
                nof_work_days=0
                leave_sal=0
                tot_leave_sal=0
                if not record.company_id.company_registry:
                    raise UserError(_("Please configure Establish number for the Branch"))
                    #print ('1111111')
                #est_number = '00000000001'
                est_number = record.company_id.company_registry
#                 comp_edr= sum_id.branch_id.wps_type +","
#                 print (comp_edr,"uuuuuuuuuuuuuuu")
                #comp_edr = 'EDR'+","
                #scr = 'SCR,'
                #scr=sum_id.branch_id.sal_control_record+","                

                empl_id = self.env['hr.payslip'].browse(ac_ids.id)
                
                f_cr_date=time.strftime("%Y-%m-%d",time.localtime(time.time()))+","
                f_cr_time=time.strftime("%H%M",time.gmtime(time.time()+19800))+","
                #sal_month=datetime.strptime(,"%m%Y")+","                
                month = datetime.strptime(record.date_end, '%Y-%m-%d').month
                year = datetime.strptime(record.date_end, '%Y-%m-%d').year
                sal_month = str(month) + str(year) +","
                if not record.slip_ids.ids:
                    raise UserError(_("No Working Employees for this branch ( %s ) \nPlease change working branch in Employee profile. !" % (sum_id.branch_id.name)))                
                
                if record.company_id.id == empl_id.employee_id.visa_branch.id:
                    start_date=empl_id.date_from
                    end_date=empl_id.date_to 
                    
                    holidays = []
                    leave_obj=self.env['hr.holidays']
                    holidays_1 = leave_obj.search([('employee_id','=',empl_id.employee_id.id),('date_from','>=',start_date),('date_from','<=',end_date),('state','=','validate')])
                    holidays_2 = leave_obj.search([('employee_id','=',empl_id.employee_id.id),('date_to','>=',start_date),('date_to','<=',end_date),('state','=','validate')])
                    #holidays = holidays_1
                    for h1 in holidays_1:
                        if h1.id not in holidays:
                            holidays.append(h1.id)
                    for h in holidays_2:
                        if h.id not in holidays:
                            holidays.append(h.id)
    
                    attendance=self.env['hr.attendance']
                    att_search_ids=attendance.search([('employee_id','=',empl_id.employee_id.id),('check_in','!=',None)])
                    
                    s_days=[]
                    for i in att_search_ids:
                        at_s=i.check_in              
                        if dateutil.parser.parse(at_s).date()>=dateutil.parser.parse(start_date).date() and dateutil.parser.parse(at_s).date()<=dateutil.parser.parse(end_date).date():                                  
                            s_days.append(at_s)  
                    sign_in_days=len(s_days)
                    
                    
                    worked_days = empl_id.paid_days if empl_id.paid_days else 0
                    
                    
                    for lea in empl_id.worked_days_line_ids:
                        if lea.code == 'LOP':
                            leave_days += lea.number_of_days
                    leave_days = int(leave_days)

                    no_of_days=sign_in_days
                    sal_perday=0
                    tot=0
                    for amt in empl_id.line_ids:
                        if amt.code == 'NET':
                            tot+=amt.total
#                         if amt.code == 'GROSS':
#                             fixed_sal += amt.total
                    no_of_days=str(no_of_days)
                    if len(no_of_days)==1:no_of_days='000'+no_of_days
                    elif len(no_of_days)==2:no_of_days='00'+no_of_days 
                    elif no_of_days==False:
                        no_of_days='0000'    
                    
#                     if empl_id.input_line_ids:
#                         for oi in empl_id.input_line_ids:
#                             var_sal+=oi.amount
                    
                    if empl_id.line_ids:
                        for head in empl_id.line_ids:
                            if head.category_id.name == 'Allowance' and head.code in ['BASIC','TA','HRA']:
                                fixed_sal += head.total
                            elif head.category_id.name == 'Allowance' and head.code not in ['BASIC','TA','HRA']:
                                var_sal += head.total
                            elif head.category_id.name == 'Deduction':
                                ded_sal += abs(head.total)
                            
                    #var_sal = var_sal - ded_sal
                    tot_sal=tot_sal+fixed_sal+var_sal 

                    # Getting Employee CODE
                    
                    if empl_id.employee_id.emp_no:
                        emp_pers_id = empl_id.employee_id.emp_no
                        if len(emp_pers_id) < 14:
                            prelen=14-len(emp_pers_id)
                            emp_pers_id = '0'*prelen+emp_pers_id
                        emp_pers_id= emp_pers_id+","
                    else:
                        raise UserError(_("Please configure Employee code for the employee %s" % (empl_id.employee_id.name)))
                        emp_pers_id= '  '+","
                    
                    # Employee Account NUmber
                    
                    if not empl_id.employee_id.bank_account_id:
                        raise UserError(_("Please configure Employee Bank Account number for the employee %s" % (empl_id.employee_id.name)))
                    
                    if empl_id.employee_id.bank_account_id.acc_number:
                        empl_acc_no = empl_id.employee_id.bank_account_id.acc_number
                        if len(empl_acc_no) < 16:
                            prelen=16-len(empl_acc_no)
                            empl_acc_no = '0'*prelen+empl_acc_no
                        empl_acc_no= empl_acc_no+","
                    else:
                        empl_acc_no = '  '+","                    
                    
                    # Bank Code
                    
                    if not empl_id.employee_id.bank_account_id.bank_id:
                        raise UserError(_("Please configure Bank details in Account number for the employee %s !" % (empl_id.employee_id.name)))
                    
                    if  empl_id.employee_id.bank_account_id.bank_id:
                        empl_bankcode= empl_id.employee_id.bank_account_id.bic_code+","
                    else:
                        empl_bankcode = '  '+","
                    
                    png_file.write(bytes('EDR,', 'utf-8'))
                    png_file.write(bytes(str(emp_pers_id), 'utf-8'))
                    png_file.write(bytes(str(empl_bankcode), 'utf-8') )
                    png_file.write(bytes(str(empl_acc_no), 'utf-8') )
                    png_file.write(bytes(str(start_date+","), 'utf-8') )
                    png_file.write(bytes(str(end_date+","), 'utf-8') )
                    png_file.write(bytes(str(abs(worked_days))+",", 'utf-8') )
                    png_file.write(bytes(str("{0:.2f}".format(abs(fixed_sal))+","), 'utf-8') )
                    png_file.write(bytes(str("{0:.2f}".format(abs(var_sal))+","), 'utf-8') )
                    png_file.write(bytes(str(abs(leave_days))+"\n", 'utf-8') )
                    n_edr+=1
                    
            if not record.company_id.company_registry:
                raise UserError(_('Please configure Company Branch!'))
#             if sum_id.bank_routing_code:
#                 company_employer_banker_code = sum_id.bank_routing_code+","   
#             else:
#                 if not sum_id.branch_id.emp_bic:
#                     raise UserError(_('Please configure Employee Banker Code in Branch!'))
            company_employer_banker_code = record.company_id.emp_bic+","
            
            company_establishment_number = record.company_id.company_registry+","
            if n_edr >= 1:
                cur_id=self.env.user.company_id.currency_id.name
                png_file.write(bytes('SCR,', 'utf-8'))
                png_file.write(bytes(company_establishment_number, 'utf-8'))
                png_file.write(bytes(company_employer_banker_code, 'utf-8'))
                png_file.write(bytes(f_cr_date, 'utf-8'))
                png_file.write(bytes(f_cr_time, 'utf-8'))
                png_file.write(bytes(sal_month, 'utf-8'))
                png_file.write(bytes(str(n_edr)+",", 'utf-8'))
                png_file.write(bytes("{0:.2f}".format(tot_sal)+",", 'utf-8'))
                png_file.write(bytes(cur_id, 'utf-8'))
                
            file_cr_date= time.strftime("%y%m%d",time.localtime(time.time()))
            f_name= str(est_number+file_cr_date+f_cr_time)
            f_name=''.join(e for e in f_name if e.isalnum())
            png_file.close()
            png_file = open(file_path, 'r+')
            data=png_file.read()
            png_file.truncate()
            png_file.close()

            attach_vals = {
            'name': '%s.sif' % (f_name),
            'datas': base64.b64encode(data.encode()),
            'datas_fname': '%s.sif' % (f_name),
            }
            doc_id = self.env['ir.attachment'].create(attach_vals)
            return {
                'type': 'ir.actions.act_url',
                'url': 'web/content/%s?download=true' % (doc_id.id),
                'target': 'self',
            }
    
    
    
class HrPayslipAttendanceDays(models.Model):
    _name = 'hr.payslip.attendance_days'
    _description = 'Payslip Attendance Days'
    _order = 'payslip_id, sequence'

    name = fields.Char(string='Description', required=True)
    payslip_id = fields.Many2one('hr.payslip', string='Pay Slip', required=True, ondelete='cascade', index=True)
    sequence = fields.Integer(required=True, index=True, default=10)
    code = fields.Char(required=True, help="The code that can be used in the salary rules")
    number_of_days = fields.Float(string='Number of Days')
    number_of_hours = fields.Float(string='Number of Hours')
    contract_id = fields.Many2one('hr.contract', string='Contract', required=True,
        help="The contract for which applied this input") 
