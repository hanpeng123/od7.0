from openerp.osv import osv,fields
#from openerp.addons.sale.wizard import sale_make_invoice_advance
class Subinvoice(osv.Model):
    
    _inherit='sale.order'
    _columns={
              'subinv_rules':fields.many2one('account.sub.invoice.rule',u"Sub Invoice Rules"),
              'use_rules':fields.boolean(u"Use Sub Invoice Rules",required=False,),
              }
    _defaults={
               'use_rules':False,
               }
    def _check_rules(self,cr,uid,ids,context=None):
        obj=self.browse(cr, uid, ids[0],context)
        if obj.use_rules and  not obj.subinv_rules:
            return False
        return True
    
    _constraints=[(_check_rules,'You must select a rule!',['Sub Invoice Rules!'])]
    

Subinvoice()

class SubinvRule(osv.Model):
    
    _name='account.sub.invoice.rule'
    _columns={
              'code':fields.char(size=30,string=u"Sub Invoice Rule code",required=True),
              'name':fields.char(size=30,string=u"Sub Invoice Rule Name",required=True),
              'autocreate':fields.boolean(u"Auto Create Sub Invoice from Sale Order"),
              'adjustment':fields.boolean(u"Adjustment Amount"),
              'rule_lines':fields.one2many('account.sub.invoice.rule.line','ruleid',u"Rule Lines"),
              }
    _defaults={
               'autocreate':True,
               'adjustment':True,
               }
    
    def _get_ruleline(self,cr,uid,ids,context=None):
        sql_str="""
        select sum(lines.amount) amount_sum from account_sub_invoice_rule rules
        inner join account_sub_invoice_rule_line lines on rules.id=lines.ruleid 
        where rules.id=%d
        """%(ids[0],)
        cr.execute(sql_str)
        sql_res=cr.dictfetchone()
        if sql_res and sql_res['amount_sum']==1:
            return True
        return False

    
    _constraints=[
                  (_get_ruleline,'Amount sum must be equal to 1 !',['Check Rules Amounts']),
                  ]


SubinvRule()    

class SubinvRuleLine(osv.Model):
    
    _name='account.sub.invoice.rule.line'
    _columns={
              'duedate':fields.date(u"Due Date",required=True),
              'amount':fields.float(u"Amount",required=True),
              'mail_reminder_days_before':fields.integer(u"Day before mail reminder"),
              'ruleid':fields.many2one('account.sub.invoice.rule',string=u"Rule id"),
              }
    _sql_constraints=[
                     ('amount_constraints','check(amount >0 and amount <=1)','Amount must between 0-1!'),
                     ('days_must_gt_zero','check(mail_reminder_days_before>0)','Days must be greater than zero!'),
                     ]
    
class InvoicePayment(osv.Model):
    
    _inherit='sale.advance.payment.inv'
    
    def _get_rule_percent(self,cr,uid,ids,context=None):
        "Get sub invoice rule percentage from sale order."
        sale_ids = context.get('active_ids', [])
        print "------------------------"
        print sale_ids
        sale_obj=self.pool.get('sale.order').browse(cr,uid,sale_ids,context)
        print "========================="
        print sale_obj.use_rules
        if sale_obj.use_rules:
            print "-----i am here......"
            return 70
        return 60
    
    _defaults={
               'amount':_get_rule_percent
               }
        
InvoicePayment()    
    