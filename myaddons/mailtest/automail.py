# -*- coding:utf-8 -*-
from openerp.osv import osv, fields

class automail(osv.Model):
    
    def _get_user_email(self,cr,uid,ids,fields,args,context=None):
        res={}
        current_id=False
        if ids:
            current_id=ids[0]
        sql="""
        select email from res_partner where id=(select partner_id from res_users where id=
        (select create_uid from hp_mailtest where id=%d)
        )
        
        """%(current_id,)
        cr.execute(sql)
        sql = cr.dictfetchone()
        if sql:
            res[current_id]=sql['email']
        else:
            res[current_id]=False
        return res
        
        
    
    _inherit='hp.mailtest'
    _columns = {
                'user_email':fields.function(_get_user_email,type='char',string=u"User Email"),
              }
    
    def create(self, cr, uid, vals, context=None):
        res=super(automail,self).create(cr, uid, vals, context=context)
        if vals:
            template = self.pool.get('ir.model.data').get_object(cr, uid, 'mailtest', 'mailtest_template')
            mail_id = self.pool.get('email.template').send_mail(cr, uid, template.id, res , force_send=True)
            
        return res
