from openerp.osv import osv,fields

class Books(osv.Model):
    
    _name='book.book'
    _columns={
              'code':fields.char(size=20,string="Code"),
              'name':fields.char(size=20,string="Name"),
              'gods':fields.boolean("Gods"),
              }
    _defaults={
               'gods':False
               }
    
Books()