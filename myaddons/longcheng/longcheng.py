# -*- coding:utf-8 -*-

from openerp.osv import osv, fields

class longcheng(osv.Model):
    
    def _get_creater(self, cr, uid, ids,field_name,args, context={}):
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

    _inherit = ['mail.thread']
    _name = 'longcheng.enterprise'
    _columns = {
              'name':fields.char(u"Enterprise Name", size=100, required=True,readonly=True,states={'draft':[('readonly',False)]}),
              'establish_date':fields.date(u"Established Date", required=True),
              'capital':fields.float(u"Capital"),
              'code':fields.char(u"Organization Code", size=100, required=True),
              'area':fields.char(u"Area", size=100, requried=True),
              'scale':fields.selection([('mini', u"Small"), ('median', u'Median'), ('large', u"Large")], u"Scale", requried=True),
              'ishightech':fields.boolean(u"Is high-tech ?"),
              'emp_num_total':fields.integer(u"Total Employees"),
              'emp_num_rd':fields.integer(u"RD Employees"),
              'faren':fields.char(u"Legal representative", size=100, required=True),
              'finleader':fields.char(u"Financial Leader", size=100, required=True),
              'faren_phone':fields.char(u"Faren Phone", size=100),
              'faren_mail':fields.char(u"Faren Mail", size=100),
              'fin_phone':fields.char(u"Finance Phone", size=100),
              'fin_mail':fields.char(u"Finance Mail", size=100),
              'patent_id':fields.one2many('longcheng.patent', 'etp_id', u"Patent information"),
              'state':fields.selection([('draft', u"New"), ('open', u"Check"), ('cancel', u"RefusedOpen"), ('offer', u"Documents for Agreement"),
                                        ('payment_request', u"PaymentRequents"), ('agreement', u"Agreement"), ('agree_agreement', u"Agree"), ('refuse_agreement', u"Refuse"),
                                        ('attach', u"Attach"), ('close', u"Done")], 'Status',
                                       readonly=True, track_visibility='onchange', required=True),
              'doc4agreement':fields.binary(u"Documents for Agreement"),
              'attach4payment':fields.binary(u"Attach for Payment"),
              'creater':fields.function(_get_creater, type='char', string=u"Creater"),
              }
    _defaults = {
               'ishightech':False,
               'state':'draft',
               }
    
    _sql_constraints = [
                      ('unique_enterprise_name', 'unique(name)', 'Enterprise name must be unique!'),
                      ]
    
    def enterprise_base_draft(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)
    
    def enterprise_base_cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def enterprise_base_open(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)
    
    def enterprise_base_offer(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'offer'}, context=context)
    
    def enterprise_base_payment_request(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'payment_request'}, context=context)
    
    def enterprise_base_refuse_agreement(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'refuse_agreement'}, context=context)
    
    def enterprise_base_agree_agreement(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'agree_agreement'}, context=context)
    
    def enterprise_base_attach(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'attach'}, context=context)

    def enterprise_base_close(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'close'}, context=context)      
    
    def enterprise_base_agreement(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state':'agreement'}, context=context)  
    
longcheng()


class patent(osv.Model):
    
    _name = 'longcheng.patent'
    _columns = {
              'name':fields.char(u"Patent Name", size=100, required=True),
              'howtoget':fields.selection([('purchase', u'Purchase'), ('own', u'Own'), ('donate', u'Donate')], u"How to get it", required=True),
              'values':fields.float(u"Patent Value"),
              'etp_id':fields.many2one('longcheng.enterprise', u"Enterprise", requird=True),
              }
    _sql_constraints = [
                      ('unique_patent_name', 'unique(name)', 'Patent name must be unique!'),
                      
                      ]

patent()