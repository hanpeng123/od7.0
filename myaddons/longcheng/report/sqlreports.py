# -*- coding:utf-8 -*-

from openerp.osv import osv, fields
from openerp import tools

class enterprisepaatent(osv.Model):
    _name = "longcheng.patentinfo"
    _auto = False
    _columns = {
            'code':fields.char(u"Enterprise Code", size=256, readonly=True),
            'etpname':fields.char(u"Enterprise Name", size=256, readonly=True),
            'establishdate':fields.date(u"Establish Date", readonly=True),
            'patentname':fields.char(u"Patent Name", size=256, readonly=True),
            'sn':fields.integer(u"SN"),
            'patentvalue':fields.float(u"Patent Value")
              }
    _order = 'code'
    
    
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'longcheng_patentinfo')
        cr.execute("""
        create or replace view longcheng_patentinfo 
        as
        (
        select p.id id,etp.code,etp.name etpname,etp.establish_date establishdate,p.name patentname ,
                count(etp.code) over(partition by etp.code rows between unbounded PRECEDING and current row) sn,
                p.values patentvalue
                from longcheng_enterprise etp
                inner join longcheng_patent p on etp.id=p.etp_id
                )
        """
        )
        

        

enterprisepaatent()
