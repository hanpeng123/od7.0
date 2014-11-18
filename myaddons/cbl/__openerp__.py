{
    'name' : 'CBL International Information managements',
    'version' : '1.0',
    'author' : 'hp',
    'category' : 'sale/invoices',
    'description' : """
    CBL International Sub invoice managements and mail reminder.
    """,
    'website': 'http://www.openerp.com',
    'images' : [],
    'depends' : ['account_accountant','sale'],
    'data': [
             'views/droprule_view.xml',
             'views/saleorder_view.xml',
             'views/board_view.xml',
             'views/book_view.xml',
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
