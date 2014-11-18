{
    'name' : 'CBL International Sub invoice managements',
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
             'views/subrule_view.xml',
             'views/saleorder_view.xml',
             'views/pp_view.xml',
             'views/board_view.xml',
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
