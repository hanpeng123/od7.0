# -*- coding:utf-8 -*-
from openerp.osv import osv,fields

class longchengbase(osv.Model):
    
    def get_creater(self, cr, uid, ids,field_name,args, context={}):
        res = {}
        for i in ids:
            sql_req = """
            select name from res_partner where id=(
            select partner_id from res_users where id=(
            select create_uid from longcheng_enterprise where id=%d
            )
            )
            """%(i,)
            cr.execute(sql_req)
            sql_req = cr.dictfetchone()
            if sql_req:
                res[i] = sql_req['name']
            else:
                res[i] = False
            
        return res
    
    def get_modifier(self, cr, uid, ids,field_name,args, context={}):
        res = {}
        for i in ids:
            sql_req = """
            select name from res_partner where id=(
            select partner_id from res_users where id=(
            select write_uid from longcheng_enterprise where id=%d
            )
            )
            """%(i,)
            cr.execute(sql_req)
            sql_req = cr.dictfetchone()
            if sql_req:
                res[i] = sql_req['name']
            else:
                res[i] = False
            
        return res
    
    _name='longcheng.base'
    _columns={
              'tsi':fields.datetime(u"Datetime"),
              }
    