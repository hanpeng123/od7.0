{
    'name' : 'Family Books Managements Module',
    'version' : '1.0',
    'author' : 'hanpeng',
    'category' : 'Family',
    'description' : """
    This module is used to manage your own books.
    """,
    'website': 'http://www.openerp.com',
    'images' : [],
    'depends' : ['mail'],
    'data': [
             'view/region_view.xml',
             'view/publisher_view.xml',
             'view/category_view.xml',
             'view/author_view.xml',
             'view/book_view.xml',
             
    ],
    'js': [
    ],
    'qweb' : [
    ],
    'css':[
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
