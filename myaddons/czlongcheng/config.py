# -*- coding:utf-8 -*-

from openerp.osv import osv,fields
class longchengconfig(osv.Model):
    
    _name='longcheng.config'
    _log_access=False
    _columns={
              'code':fields.char(u"Code",size=100,required=True),
              'name':fields.char(u"Investment Code Rule",size=100,required=True),
              }
    _sql_constraint=[
                     ('unique_config_code','unqiue(code)','Config code must be unuqie!'),
                     ]
longchengconfig()