# -*- coding:utf-8 -*-
from openerp.osv import osv, fields

class ParentWindow(osv.Model):
    
    _name = 'test.parent.window'
    _columns = {
              'code':fields.char(size=20, string=u"Code"),
              'name':fields.char(size=20, string=u"Name"),
              }
    
    def open_child(self, cr, uid, ids, context=None):
        p_obj=self.browse(cr, uid, ids[0],context)
        
        ir_model_data = self.pool.get('ir.model.data')
        compose_form_id = ir_model_data.get_object_reference(cr, uid, 'subinvoice', 'pc_form_view')[1]
        ctx = dict(context)
        ctx.update({
            'default_code':p_obj.code,
            'default_name':p_obj.name,
        })    
        return {
            'name':'Open child Form',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'test.child.window',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'nodestroy': True,
            'target': 'new',
            'context': ctx,
        }
       
ParentWindow()

class ChildWindow(osv.Model):
    
    def _get_parent_window(self, cr, uid, ids, context=None):
        if context is None:
            context={}
        cid=context.get('current_id',[])
        print '========================='
        print cid
        return cid

        
    
    _name = 'test.child.window'
    _columns = {
              'code':fields.char(size=20, string=u"Code"),
              'name':fields.char(size=20, string=u"Name"),
              }
    _default={
              'code':_get_parent_window,
              }
