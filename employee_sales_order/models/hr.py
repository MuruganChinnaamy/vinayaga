# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017-Today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api, fields, models, _

class Employee(models.Model):

    _inherit = "hr.employee"

    sales_order_count = fields.Integer(compute='_compute_sales_order', string='Number of Sales Order')
    sales_order_stages = fields.Char(compute='_compute_sales_order', string='Sales Order Status')

    def _compute_sales_order(self):
        for employee in self:
            user = employee.user_id
            if user:
                orders = self.env['sale.order'].sudo().search([('user_id','=',user.id)])
                employee.sales_order_count = str(len(orders))
                tt_order = {}
                count = 0
                order_state_text = ''
                for order in orders:
                    if order.state not in tt_order:
                        value = dict(self.env['sale.order'].fields_get(allfields=['state'])['state']['selection'])[order.state]
                        tt_order.update({value:0})
                    state_orders = self.env['sale.order'].sudo().search([('user_id','=',user.id),('state','=',order.state)])
                    tt_order[value] = len(state_orders)
                for item in tt_order:
                    if tt_order[item] != 0:
                        if order_state_text:
                            order_state_text = order_state_text + ' | ' + item + ': ' + str(tt_order[item])
                        else:
                            order_state_text =  item + ': ' + str(tt_order[item])
                employee.sales_order_stages = order_state_text

    @api.multi
    def display_employee_sales_order(self):
        """Display employee sales order"""
        if self.user_id:
            context="{'group_by':'state'}"
            template_id = self.env.ref('sale.view_order_tree').id
            search_id = self.env.ref('sale.sale_order_view_search_inherit_sale').id
            return {
                'name': _('Employee Sales Order'),
                'view_type': 'form',
                'view_mode': 'kanban,tree,calendar,pivot,graph,form',
                'res_model': 'sale.order',
                'type': 'ir.actions.act_window',
                'view_id': template_id,
                'views': [(self.env.ref('sale.view_order_tree').id, 'tree'),
                          (self.env.ref('sale.view_order_form').id, 'form'),
                          (self.env.ref('sale.view_sale_order_kanban').id, 'kanban'),
                          (self.env.ref('sale.view_sale_order_calendar').id, 'calendar'),
                          (self.env.ref('sale.view_sale_order_pivot').id, 'pivot'),
                          (self.env.ref('sale.view_sale_order_graph').id, 'graph')],
                'search_view_id': search_id,
                'domain': [('user_id','=',self.user_id.id)],
                'context': context
             }



