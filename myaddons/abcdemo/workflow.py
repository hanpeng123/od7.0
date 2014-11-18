# -*- coding:utf-8 -*-
from openerp.osv import osv,fields

class workflowtest01(osv.Model):
    
    def test_email(self, cr, uid, ids, context=None):
        ir_model_data = self.pool.get('ir.model.data')
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False 
        return {
            'name':'Here we test to send a email...',
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
    
    _inherit='mail.thread'
    _name="amt.wfl01"
    _columns={
              'code':fields.char(u"Code",size=100,required=True),
              'name':fields.char(u"Name",size=100,required=True),
              'state':fields.selection([('draft',u"Draft"),('process',u"Process"),('done',u'Done')],u"status",
                                       track_visibility='onchange',required=True,readonly=True),
              }
    _defaults={
               'state':'draft',
               }
    
    def amt_test_draft(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)
    
    def amt_test_process(self, cr, uid, ids, context={}):
        res={}
        self.write(cr, uid, ids, {'state': 'process'}, context=context)
        return res


    def amt_test_done(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'done'}, context=context)

workflowtest01()

class workflowtest02(osv.Model):
    
    _inherit='mail.thread'
    _name="amt.wfl02"
    _columns={
              'code':fields.char(u"Code",size=100,required=True),
              'name':fields.char(u"Name",size=100,required=True),
              'state':fields.selection([('doc',u"Document"),('agreement',u"Agreement"),('payment',u'payment')],u"status",
                                       track_visibility='onchange',required=True,readonly=True),
              }
    _defaults={
               'state':'doc',
               }
    def amt_test_doc(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'doc'}, context=context)
    
    def amt_test_agreement(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'agreement'}, context=context)

    def amt_test_payment(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'payment'}, context=context)

workflowtest02()

class workflowtest03(osv.Model):
    
    _inherit='mail.thread'
    _name="amt.wfl03"
    _columns={
              'code':fields.char(u"Code",size=100,required=True),
              'name':fields.char(u"Name",size=100,required=True),
              'state':fields.selection([('draft',u"Draft"),('process',u"Process"),('done',u'Done')],string=u"state",required=True),
              }

workflowtest03()