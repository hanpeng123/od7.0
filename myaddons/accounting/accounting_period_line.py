# -*- coding:utf-8 -*-
from openerp.osv import osv,fields

class Thp(osv.Model):
    _name='hp.hp'
    _columns={
              'name':fields.char(size=20,string=u"Name"),
              'code':fields.char(size=20,string=u"Code"),
              }