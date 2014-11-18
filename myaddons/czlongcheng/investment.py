# -*- coding:utf-8 -*-
from openerp.osv import osv,fields
from openerp.addons.email_template import email_template

class Corp(osv.Model):
    
    _name='longcheng.corp'
    _columns={
              'code':fields.char(u"Code",size=100,required=True),
              'name':fields.char(u"Name",size=100,required=True),
              }
    _sql_constraints=[('unique_corp_code','unique(code)','Company code must be unique!'),
                      ('unique_corp_name','unique(name)','Company name must be unique!'),
                      ]

Corp()

class Region(osv.Model):
    
    def _get_area_depth(self, cr, uid, ids, fields, args, context=None):
        res = {}
        if not ids:
            return False
        for i in ids:
            sql_res = """
            with RECURSIVE areas(rid,p_rid,code,region_name,depth) as (
              select id rid,parent_region p_rid,code,name region_name,1 deptth from longcheng_region where id=%d
              union ALL
              select region.id,region.parent_region,region.code,region.name,depth+1    
              from areas,longcheng_region region where areas.p_rid=region.id
            )
            select region_name from areas order by depth desc           
            """ % (i,)
            cr.execute(sql_res)
            sql_res = cr.dictfetchall()
            if sql_res:
                res[ids[0]] = ""
                for line in sql_res:
                    res[ids[0]] += line['region_name'] + '>'
            else:
                res[ids[0]] = "None"
        return res
    
    _name = 'longcheng.region'
    _columns = {
              'code':fields.char(u"Code", size=50, required=True),
              'name':fields.char(u"Name", size=50, required=True),
              'parent_region':fields.many2one('longcheng.region', u"Parent Region"),
              'region_path':fields.function(_get_area_depth,type='char',string=u"Region Path"),
              }
    _sql_constraints = [
                      ('unique_region_code', 'unique(code)', 'Region code must be unique!'),
                      ]
    


class Investment(osv.Model):
    
    def _get_user_email(self,cr,uid,ids,fields,args,context=None):
        res={}
        current_id=False
        if ids:
            current_id=ids[0]
        sql="""
        select email from res_partner where id=(select partner_id from res_users where id=
        (select create_uid from longcheng_invetstment where id=%d)
        )
        
        """%(current_id,)
        cr.execute(sql)
        sql = cr.dictfetchone()
        if sql:
            res[current_id]=sql['email']
        else:
            res[current_id]=False
        return res
    
    
    def send_email(self, cr, uid, ids, context=None):
        
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        ir_model_data = self.pool.get('ir.model.data')
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'mailtest', 'mailtest_template')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False 
        ctx = dict(context)
        ctx.update({
            'default_model': 'hp.mailtest',
            'default_res_id': ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            #'mark_so_as_sent': True
        })    
        return {
            'name':'Mail Test Form',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'nodestroy': True,
            'target': 'new',
            'context': context,
        }
    
    def get_creater(self, cr, uid, ids,field_name,args, context={}):
        res = {}
        for i in ids:
            sql_req = """
            select name from res_partner where id=(
            select partner_id from res_users where id=(
            select create_uid from longcheng_invetstment where id=%d
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
            select write_uid from longcheng_invetstment where id=%d
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
    
    def get_creater_time(self, cr, uid, ids,field_name,args, context={}):
        res = {}
        for i in ids:
            sql_req = """
            select create_date cdate from  longcheng_invetstment where id=%d
            """%(i,)
            cr.execute(sql_req)
            sql_req = cr.dictfetchone()
            if sql_req:
                res[i] = sql_req['cdate']
            else:
                res[i] = False
            
        return res
    
    def get_modifier_time(self, cr, uid, ids,field_name,args, context={}):
        res = {}
        for i in ids:
            sql_req = """
            select write_date wdate from  longcheng_invetstment where id=%d
            """%(i,)
            cr.execute(sql_req)
            sql_req = cr.dictfetchone()
            if sql_req:
                res[i] = sql_req['wdate']
            else:
                res[i] = False
            
        return res
    
    def get_voucher_no(self,cr, uid, ids,field_name,args, context={}):
        res = {}
        for i in ids:
            sql_req = """
            select 'Investment-'||lpad(to_char(nextval('inv_sq'),'FM999MI'),5,'0') num
            """
            cr.execute(sql_req)
            sql_req = cr.dictfetchone()
            if sql_req:
                res[i] = sql_req['num']
            else:
                res[i] = False
            
        return res
    
    _inherit=['mail.thread']
    _name='longcheng.invetstment'
    _columns={
              'code':fields.char(u"Project Code",size=100,required=True,readonly=True,states={'draft':[('readonly',False)]}),
              'name':fields.char(u"Project Name",size=100,required=True,readonly=True,states={'draft':[('readonly',False)]}),
              'total_amount':fields.integer(u"Total Amount",readonly=True,states={'draft':[('readonly',False)]},groups="czlongcheng.group_investment_readonly,czlongcheng.group_investment_approveall"),
              'email':fields.char(u"Email",size=100,readonly=True,states={'draft':[('readonly',False)]}),
              'voucherno':fields.function(get_voucher_no,type='char',string=u"Voucher Number",store=True),
              'corp_id':fields.many2one('longcheng.corp',u"Company",required=True,readonly=True,states={'draft':[('readonly',False)]}),
              'shenqing_date':fields.date(u"Applying date",required=True,readonly=True,states={'draft':[('readonly',False)]}),
              'introduction':fields.text(u"Project Instroduction",readonly=True,states={'draft':[('readonly',False)]}),
              'docs4proj':fields.binary(u"Documents for project",readonly=True,states={'draft':[('readonly',False),('required',True)]}),
              'docs4ddi':fields.binary(u"Documents for DDI",invisible=True,readonly=True,states={'ddi':[('required',True),('readonly',False),('invisible',False)]}),
              'state':fields.selection([('draft',u"Draft"),
                                        ('open',u'Open'),
                                        ('lc',u'Longcheng workflow'),
                                        ('group',u"Longcheng Group"),
                                        ('approve',u'Approve'),
                                        ('approve_refuse',u'Refuse Approve'),
                                        ('ddi',u"DDI"),
                                        ('fupan',u"Fupan"),
                                        ('pingshen',u"Pingshen"),
                                        ('toushen',u"Toushen"),
                                        ('guohui',u"Guohui"),
                                        ('guohui_refuse',u"Refuse Guohui"),
                                        ('enterprise',u"Enterprise "),
                                        ('cancel',u'Cancel'),
                                        ('done',u"Done")],
                                       u"Status",readonly=True,required=True,track_visibility='onchange'),
              'comments':fields.text(u"Commnets",states={
                                                         'done':[('readonly',True)],
                                                         'draft':[('invisible',True)],
                                                         'cancel':[('readonly',True)],
                                                         'guohui_refuse':[('readonly',True)],
                                                         'approve_refuse':[('readonly',True)]
                                                         }),
              'dummy_comments':fields.text(u"Dummy Comments"),
              'status_log':fields.char(u"Status_log",invisible=False,size=100),
              'comm_ids':fields.one2many('longcheng.investment.comment','invest_id',u"History Comments"),
              'sub_ids':fields.one2many('longcheng.enterprise','main_no',u"Subflows"),
              'creator':fields.function(get_creater,type='char',string=u"Creator"),
              'modifier':fields.function(get_modifier,type='char',string=u'Modifier'),
              'cdate':fields.function(get_creater_time,type='char',string=u"Created datetime"),
              'wdate':fields.function(get_modifier_time,type='char',string=u"Moidified datetime"),
              'user_email':fields.function(_get_user_email,type='char',string=u"User Email"),
              }
    _defaults={
               'state':'draft',
               }
    _sql_constraints=[
                      ('unique_inv_code','unique(code)','Investment code must be unique!'),
                      ]
    
    def invest_action_subflow(self,cr,uid,ids,context={}):
        #Firstly, Enterprise information must be filled.
        #If the enterprise info has been filled,just open it and need not generate an new instance.
        sub_flow=self.pool.get('longcheng.enterprise')
        curr_info=self.browse(cr, uid, ids, context)
        corpinfo=[obj.corp_id.id for obj in curr_info]
        voucherinfo=[obj.voucherno for obj in curr_info]
        subids=[obj.sub_ids for obj in curr_info]
        subid=0
        if not len(subids[0]):
            subid=sub_flow.create(cr,uid,{'code':voucherinfo[0]+'[You must modify it]','corp_id':corpinfo[0],
                                      'main_no':ids[0],'establish_date':'2013-09-08','faren':'Faren','finleader':'Finleader'},context)
        else:
            subid=subids[0]
            subid= subid[0].id
        #here we assume that one main workflow has only one subflow.
        #If not ,'=' in line 251 shoud be replace with 'in'.
        #Secondly,Find the enterprise action and open it with the id above.
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result = mod_obj.get_object_reference(cr, uid, 'czlongcheng', 'enterprise_base_actions')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        result['domain'] = "[('id','=',"+str(subid)+")]"
        return result
    
    def investment_draft(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'draft','status_log':'Draft'}, context=context)
    
    def investment_open(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'open','status_log':'Open'}, context=context)
    
    def investment_lc(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'lc','status_log':'Longcheng Yingcai Workflow'}, context=context)
    
    def investment_group(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'group','status_log':'Logncheng Group Workflow'}, context=context)
    
    def investment_approve(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'approve','status_log':'Approve'}, context=context)
    
    def investment_approve_refuse(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'cancel','status_log':'Approve Refused'}, context=context)
    
    def investment_ddi(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'ddi','status_log':'DDI'}, context=context)
    
    def investment_fupan(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'fupan','status_log':'Fupan'}, context=context)
    
    def investment_pingshen(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'pingshen','status_log':'Pingshen'}, context=context)
    
    def investment_toushen(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'toushen','status_log':'Toushen'}, context=context)
    
    def investment_guohui(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'guohui','status_log':'Guohui'}, context=context)
    
    def investment_cancel(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'cancel','status_log':'Cancel'}, context=context)
    
    def investment_done(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'done','status_log':'Done'}, context=context)
    
    def investment_enterprise(self, cr, uid, ids, context={}):
        self.write(cr, uid, ids, {'state': 'enterprise','status_log':'Enterprise Base Information'}, context=context)
        return False
    
    def investment_guohui_refuse(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {'state': 'guohui_refuse','status_log':'Guohui Refused.'}, context=context)
    
    def message_update(self, cr, uid, ids, msg_dict, update_vals=None, context=None):
        return False
    
    def message_new(self, cr, uid, msg_dict, custom_values=None, context=None):
        return False
    
Investment()

class Investmentcomments(osv.Model):
    
    _name='longcheng.investment.comment'
    _log_access=False
    _columns={
              'invest_id':fields.many2one('longcheng.invetstment',u"Investment Workflow No."),
              'ts':fields.datetime(u"Timestamp"),
              'userid':fields.many2one('res.users',u"User"),
              'comments':fields.text(u"Comments"),
              'statuslog':fields.text(u"Status Logs"),
              }
Investmentcomments()