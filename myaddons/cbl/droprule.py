# -*- coding:utf-8 -*-
from openerp.osv import osv,fields
import datetime


class Droprule(osv.Model):
    
    _name='cbl.dropout.rule'
    _columns={
              'code':fields.char(size=20,required=True,string=u"Rule Code"),
              'name':fields.char(size=20,required=True,string=u"Rule Name"),
              'line_ids':fields.one2many('cbl.dropout.rule.line','ruleid',u"Line IDs"),
              
              }
Droprule()

class Dropruleline(osv.Model):
    
    _name='cbl.dropout.rule.line'
    _columns={
              'days':fields.integer(u"Days"),
              'action':fields.selection([('mail',u'Send Email'),('dropout',u"Dropout")],
                                        u"Action",required=True),
              'ruleid':fields.many2one('cbl.dropout.rule',u"Ruleid"),
              }
    _sql_constraints=[
                      ('days_gt_zero','check(days>0)','Days must be greater than zero!'),
                      ]   
Dropruleline() 

class Saleorder(osv.Model):
    
    def _get_payment_count(self,cr,uid,ids,context=None):
        sql_str="""
        select count(id) idc from account_voucher_line
         where name in 
          (select number from account_invoice where origin in 
           (select name from sale_order where id=%d))
        """%(ids[0],)
        cr.execute(sql_str)
        sql_res=cr.dictfetchone()
        return sql_res['idc'] 
    
    def _get_invoice_count(self,cr,uid,ids,context=None):
        sql_str="""
        select count(id) idc from account_invoice where origin in 
           (select name from sale_order where id=%d)
        """%(ids[0],)
        cr.execute(sql_str)
        sql_res=cr.dictfetchone()
        return sql_res['idc']
    
    def _get_dropout_reminder(self,cr,uid,ids,fields,args,context=None):
        res={}
        for i in ids:
            
            if self._get_payment_count(cr,uid,ids,context)==0 and self._get_invoice_count(cr,uid,ids,context)==1:
                res[i]=True
            else:
                res[i]=False
        return res
    
    _inherit='sale.order'
    _columns={
             'reminder':fields.function(_get_dropout_reminder,
                                        type='boolean',string=u"Reminder",readonly=True),
             'rule_id':fields.many2one('cbl.dropout.rule',string=u"Dropout Rule"),
             'rule_line_ids':fields.one2many('cbl.mail.recorder','sale_id',u'Mail Remainder Information',readonly=True),
             'reminder_new':fields.boolean(u"Reminder new"),  #function值在TREEVIEW和SEARCH VIEW的CONTEXT上无法正确读取。
             }
    
    _defaults={
               'reminder_new':False,
               }
    
    def _generate_sale_order_mailrecorder(self,cr,uid,rule_id,context=None):
        if not rule_id:
            return False
        ## fecth the rule line ids from rule line table.
        rule_line_ids=[]
        sql_str="""
        select id from cbl_dropout_rule_line where ruleid =%d
        """%(rule_id,)
        cr.execute(sql_str)
        sql_res=cr.fetchall()
        for i in sql_res:
            rule_line_ids.append(i[0])
        return rule_line_ids

        
    
    def create(self, cr, uid, vals, context=None):
        #if user selects a rule,record the rule information.
        if vals['rule_id']:
            line_val=[]
            rule_line_ids=self._generate_sale_order_mailrecorder(cr, uid, vals['rule_id'], context)
            for i in rule_line_ids:
                current_line=[]
                current_line.append(0)
                current_line.append(False)
                current_line.append({'mailstatus':False,'rule_line_id':i,'ts':datetime.datetime.now(),'date_order':vals['date_order'],})
                line_val.append(current_line)
            vals['rule_line_ids']=line_val
        return super(Saleorder, self).create(cr, uid, vals, context=context)
    
    def action_reminder_send(self,cr,uid,ids,context=None):
        pass
    
Saleorder()

class MailRecorder(osv.Model):
    
    _name='cbl.mail.recorder'
    _columns={
              'sale_id':fields.many2one('sale.order',u"Sale ID"),
              'rule_line_id':fields.many2one('cbl.dropout.rule.line',u'Rule line id'),
              'mailstatus':fields.boolean(u'Mail Sent Status'),
              'date_order':fields.date(u"Date Order"),
              'ts':fields.datetime(u"Timestamp"),
              }
    _defaults={
               'mailstatus':False,
               }
    
MailRecorder()