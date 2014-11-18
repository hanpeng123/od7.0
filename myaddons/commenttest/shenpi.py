# -*- coding:utf-8 -*-
from openerp.osv import osv,fields

class Shenpi(osv.Model):
    
    _name='oa.shenpi'
    _columns={
              'code':fields.char(u"Code",size=100,required=True),
              'name':fields.char(u"Name",size=100,required=True),
              'comments':fields.text(u"Comments"),      
              'dummy_comments':fields.text(u"Dummy Comments"),
              'comm_ids':fields.one2many('oa.comment','shenpi_id',u"Comments Details"),        
              }
Shenpi()

class Comment(osv.Model):
    
    _name='oa.comment'
    _columns={
              'shenpi_id':fields.many2one('oa.shenpi',u"Shenpi Information"),
              'comments':fields.text(u"Comments"),
              }  
    _sequence='mysq'  
    _log_access=False
    
Comment()