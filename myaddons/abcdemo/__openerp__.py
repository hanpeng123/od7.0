{
    'name' : 'amt test',
    'version' : '1.0',
    'author' : 'hp',
    'category' : 'test',
    'description' : """
    This is a test app.
    """,
    'website': 'http://www.openerp.com',
    'images' : [],
    'depends' : ['mail'],
    'data': [
             'test_view.xml',
             #'test_mail_template.xml',
             'wfl_view.xml',
             'test_workflow.xml',
             'test_workflow2.xml',
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
