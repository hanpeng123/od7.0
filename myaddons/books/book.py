# -*- coding:utf-8 -*-
from openerp.osv import osv, fields
from openerp import tools, SUPERUSER_ID
import time
import datetime



class region(osv.Model):
    _name = 'book.region'
    _columns = {
              'code':fields.char(u"Code", size=50, required=True),
              'name':fields.char(u"Name", size=50, required=True),
              'parent_region':fields.many2one('book.region', u"Parent Region"),
              }
    _sql_constraints = [
                      ('unique_region_code', 'unique(code)', 'Region code must be unique!'),
                      ]
    

class publisher(osv.Model):
    
    _name = 'book.publisher'
    _columns = {
              'name':fields.char(u"Name", size=50, required=True),
              'address':fields.char(u"Address", size=150),
              'reg_id':fields.many2one('book.region', u"Region", required=True),
              
              
              }
    _sql_constraints = [
                      ('unique_publisher_name', 'unique(name)', 'Publisher name must be unique!'),
                      ]
    
publisher()


class category(osv.Model):
    _name = 'book.category'
    _columns = {
              'name':fields.char(u"Name", size=100, required=True),
              'parent_category':fields.many2one('book.category', u"Parent Category"),
              'status':fields.boolean(u"Is Block?"),
              }
    _defaults = {
               'status':False
               }
    _sql_constraints = [
                      ('unique_cate_name', 'unique(name)', 'Category name must be unique!'),
                      ]
category()


class author(osv.Model):
    
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
    
    def _get_area_depth(self, cr, uid, ids, fields, args, context=None):
        res = {}
        obj = self.browse(cr, uid, ids[0])
        area_ids = (obj['area']['id'],)
#         print "-------------"
#         print obj['area']
#         print type(obj['area'])
#         print type(obj['area']['id'])
#         print "area_id:"
#         print area_ids
        for i in area_ids:
            print "-----..here.."
            sql_res = """
            with RECURSIVE areas(rid,p_rid,code,region_name,depth) as (
              select id rid,parent_region p_rid,code,name region_name,1 deptth from book_region where id=%d
              union ALL
              select region.id,region.parent_region,region.code,region.name,depth+1    
              from areas,book_region region where areas.p_rid=region.id
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
                
    
    def _get_author_age(self, cr, uid, ids, fields, args, context=None):
        res = {}
        if context is None:
            context = {}
            DATE_FORMAT = "%Y-%m-%d"
        for i in ids:
            obj = self.browse(cr, uid, i)
            date_birth = obj['birthday']
            date_death = obj['deathday']
            if date_death:
                date_death = time.strptime(date_death, "%Y-%m-%d")
                date_death = datetime.datetime(*date_death[0:3])
                date_birth = time.strptime(date_birth, "%Y-%m-%d")
                date_birth = datetime.datetime(*date_birth[0:3])
                date_diff = date_death - date_birth
                res[i] = str(round(date_diff.days / 365.0, 2)) + " years old."
            else:
                res[i] = "still alive."

        return res
            
    _inherit = 'mail.thread'
    _name = 'book.author'
    _columns = {
              'name':fields.char(u"Name", size=100, required=True),
              'birthday':fields.date(u"Birth Date", required=True),
              'deathday':fields.date(u"Death Date"),
              'age':fields.function(_get_author_age, type='char', string=u"Age"),
              'region_depth':fields.function(_get_area_depth, type='char', string=u"Region Depth"),
              'area':fields.many2one('book.region', u"Area", required=True),
              'isastranlator':fields.boolean(u"Is a Translator?"),
              'gender':fields.selection([('male', u'Male'), ('female', u'Female')], u"Gender", required=True),
              'introduction':fields.text(u"Introduction"),
              'book_ids':fields.one2many('book.book','auth_id',u"Books"),
              'image': fields.binary("Image",
                    help="This field holds the image used as image for the author, limited to 1024x1024px."),
              'image_medium': fields.function(_get_image, fnct_inv=_set_image,
                    string=u"Portrait", type="binary", multi="_get_image",
                    store={
                        'book.author': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
                    },
                    help="Medium-sized image of the author. It is automatically "\
                         "resized as a 128x128px image, with aspect ratio preserved, "\
                         "only when the image exceeds one of those sizes. Use this field in form views or some kanban views."),
              'image_small': fields.function(_get_image, fnct_inv=_set_image,
                        string=u"Portrait", type="binary", multi="_get_image",
                        store={
                            'book.author': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
                        }, help="Small-sized image of the product. It is automatically "\
                         "resized as a 64x64px image, with aspect ratio preserved. "\
                         "Use this field anywhere a small image is required."),
              
              }
    _sql_constraints = [
                      ('unique_author_name', 'unique(name)', 'Author name must be unique!'),
                      ('death_gt_birth', 'check(birthday<deathday or deathday is null)', 'Birthday must be less than death day,or death day is null.'),
                      ]
    _defaults = {
               'isastranlator':False,
               'gender':'male',
               }
    
author()

class book(osv.Model):
    
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
    
    _inherit='mail.thread'
    _name = 'book.book'
    _columns = {
              'isbn':fields.char(u"ISBN", size=20, required=True),
              'name':fields.char(u'Book Name', size=100, required=True),
              'auth_id':fields.many2one('book.author', u"Author", required=True),
              'tran_id':fields.many2many('book.author', 'book_author_rel', 'bookid', 'tran_id', u"Translator(s)"),
              'pub_ids':fields.many2many('book.publisher', 'book_publisher_rel', 'bookid', 'pub_id', u"Publisher(s)", required=True),
              'cat_ids':fields.many2many('book.category', 'book_category_rel', 'bookid', 'cate_id', 'Category', required=True),
              'word_number':fields.integer(u"Word Number", required=True),
              'price':fields.float(u"Price"),
              'booknumber':fields.integer(u"Book Number", required=True),
              'howtoget':fields.selection([('purchase', u'Purchase'), ('donate', u'Donate')], u"How to get", required=True),
              'gotdate':fields.date(u"Date Got"),
              'introduction':fields.text(u"Introduction"),
              'medium':fields.selection([('paper', u"Paper"), ('ebook', u'Electronic')], u"Book Medium", required=True),
              'state':fields.selection([('purchased', u"Purchased"), ('reading', u'Reading'), ('done', u'Read Done')], u"Reading Status", required=True),
              'image': fields.binary("Image",
                    help="This field holds the image used as image for the product, limited to 1024x1024px."),
              'image_medium': fields.function(_get_image, fnct_inv=_set_image,
                    string=u"Portrait", type="binary", multi="_get_image",
                    store={
                        'book.book': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
                    },
                    help="Medium-sized image of the book. It is automatically "\
                         "resized as a 128x128px image, with aspect ratio preserved, "\
                         "only when the image exceeds one of those sizes. Use this field in form views or some kanban views."),
              'image_small': fields.function(_get_image, fnct_inv=_set_image,
                        string=u"Portrait", type="binary", multi="_get_image",
                        store={
                            'book.book': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
                        }, help="Small-sized image of the book. It is automatically "\
                         "resized as a 64x64px image, with aspect ratio preserved. "\
                         "Use this field anywhere a small image is required."),
              }
    _defaults = {
               'state':'purchased',
               'medium':'paper',
               'booknumber':1,
               }
    _sql_constraints = [
                      ('unique_isbn', 'unique(isbn)', 'ISBN must be unique!'),
                      ('word_num_gt_1', 'check(word_number>=1)', 'Word number must not be less than 1!'),
                      ('price_gt_0', 'check(price>0)', 'Price must great than 0!'),
                      ]
book()


    
                      
                      
                    
