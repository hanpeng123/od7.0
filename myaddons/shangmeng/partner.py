# -*- coding:utf-8 -*-
from openerp.osv import osv,fields

class smpartner(osv.Model):
    
    _inherit='res.partner'
    _columns={
              'xiaoren':fields.many2one('res.partner',string=u"Xiaoren"),
              'guiren':fields.many2many('res.partner','partner_guiren_rel','guiren',
                                       'partner_id',u"Guiren"),
              'company_stage':fields.selection([('l1','Chengzhang'),('l2','Gaosukuozhangqi'),
                                                ('l3','Wendingfazhangqi'),('l4','Shuaituiqi')],string=u"Company Stage"),
              }