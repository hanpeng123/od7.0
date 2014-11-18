# -*- coding:utf-8 -*-

from openerp.osv import fields, osv
from openerp.addons.email_template import email_template

class hptest(osv.Model):
    
    def test_email(self, cr, uid, ids, context=None):
        ir_model_data = self.pool.get('ir.model.data')
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False 
        return {
            'name':'Amt Form',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'nodestroy': True,
            'target': 'new',
            'context': context,
        }
    
    def test_pop_window(self, cr, uid, ids, context=None):
#         assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        ir_model_data = self.pool.get('ir.model.data')
#         try:
#             template_id = ir_model_data.get_object_reference(cr, uid, 'abcdemo', 'email_template_edi_test')[1]
#         except ValueError:
#             template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'abcdemo', 'amt_form_form_view')[1]
        except ValueError:
            compose_form_id = False 
#         ctx = dict(context)
#         ctx.update({
#             'default_model': 'amt.form',
#             'default_res_id': ids[0],
#             'default_use_template': bool(template_id),
#             'default_template_id': template_id,
#             'default_composition_mode': 'comment',
#         })
        return {
            'name':'Amt Form',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'amt.form',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'flags': {'form': {'action_buttons': True}},
            'nodestroy': True,
            'target': 'new',
            'context': context,
        }
    
    _inherit='mail.thread'
    _name='amt.test'
    _columns={
              'code':fields.char(u"Code",size=100,required=True),
              'name':fields.char(u"Name",size=100,reruired=True),
              'mailaddress':fields.char(u"Mail address",size=100),
              }
    
hptest()

class hpform(osv.Model):
    
    
    _inherit = ['mail.thread']
    _name='amt.form'
    _columns={
              'code':fields.char(u"Code",size=100,required=True),
              'name':fields.char(u"Name",size=100,reruired=True),
              }
    
hpform()