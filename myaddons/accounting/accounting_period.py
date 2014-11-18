# -*- coding:utf-8 -*-
import time
#import datetime
from openerp.osv import osv,fields

class AccTools():
    def get_current_year_day(self,symble):
        #0,the first day of the year
        #1,the last ay of the year.
        ticks=time.localtime(time.time())
        ticks= ticks[0]
        ##
        if symble==0:
            #ticks='time'+str(ticks)+'-01'+'-01'
            ticks=str(ticks)+'-01'+'-01'
        elif symble==1:
            #ticks='time'+str(ticks)+'-12'+'-31'
            ticks=str(ticks)+'-12'+'-31'
        #return
        #ticks = time.strptime(ticks, "time%Y-%m-%d")
        #return datetime.date(ticks[0],ticks[1],ticks[2])
        return ticks
    
    def get_current_year(self):
        ticks=time.localtime(time.time())
        ticks= ticks[0]
        return ticks
    
    def get_current_datetime(self):
        ticks=time.localtime(time.time())
        return str(ticks[0])+'-'+str(ticks[1])+'-'+str(ticks[2])+' '+str(ticks[3])+':'+str(ticks[4])+':'+str(ticks[5])
        
    

class AccPeriod(osv.Model):
    
    actools=AccTools()
    
    _first_day_of_year=actools.get_current_year_day(0)
    _last_day_of_year=actools.get_current_year_day(1)
    
    
    def _get_default_fy_name(self, cr, uid, ids, context=None):
        actools=AccTools()
        _current_year=actools.get_current_year()
        return 'Financial Year '+str(_current_year)
    
    def _get_default_fy_code(self, cr, uid, ids, context=None):
        actools=AccTools()
        _current_year=actools.get_current_year()
        return 'FY'+str(_current_year)
    def _get_default_current_datetime(self,cr,uid,ids,context=None):
        actools=AccTools()
        return actools.get_current_datetime()
    
    _name='accounting.fiscal.year'
    _columns={
              'name':fields.char(size=20,required=True,string=u'Accounting Fiscal Year'),
              'code':fields.char(size=20,required=True,string=u'Accounting Period Code'),
              'date_start':fields.date(string=u'Date Start',required=True),
              'date_end':fields.date(string=u'Date End',required=True),
              'active':fields.boolean(u'Status'),
              'ts':fields.datetime(u"Time stamp"),
              }
    
    _defaults={
               'active':False,
               'date_start':_first_day_of_year,
               'date_end':_last_day_of_year,
               'name':_get_default_fy_name,
               'code':_get_default_fy_code,
               'ts':_get_default_current_datetime
               }
    _sql_constraints=[
                      ('unique_fy_name','unique(name)','Fiscal Year name must be unique!'),
                      ('unique_fy_code','unique(code)','Fiscal Year code msut be unique!'),
                      ('start_great_than_end_date','check(date_start<date_end)','Date start is must less than date end!'),                    
                      ]
    
    def onchange_name(self,cr,uid,ids,code,context=None):
        return {'value':{'name':code+'hanpeng'}}
    
    def check_date(self,cr,uid,ids,context=None):
        return self.write(cr, uid, ids, {'name':'i have changed it.','code':'hha'}, context=context)
    
    def test_popwindow(self,cr,uid,ids,context=None):
        ir_model_data = self.pool.get('ir.model.data')
        compose_form_id = ir_model_data.get_object_reference(cr, uid, 'accounting', 'pe_line_tree')[1]
        return {
            'name':'Mail Test Form',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hp.hp',
            'views': [(compose_form_id, 'tree')],
            'view_id': compose_form_id,
            'nodestroy': True,
            'target': 'new',
            'context': context,
        }

