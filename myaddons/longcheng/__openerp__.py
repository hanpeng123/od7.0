{
    'name' : 'Changzhou Longcheng Yingcai Investment Workflow',
    'version' : '1.0',
    'author' : 'hp',
    'category' : 'workflow',
    'description' : """
    This is a workflow for longcheg yingcai.
    """,
    'website': 'http://www.openerp.com',
    'images' : [],
    'depends' : ['mail'],
    'data': [
             'view/enterprise_view.xml',
             'etp_base_workflow.xml',
             'view/enterprise_view.xml',
             'report/sqlreport_view.xml',
             'security/enterprise_security.xml',
             'security/ir.model.access.csv',
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
