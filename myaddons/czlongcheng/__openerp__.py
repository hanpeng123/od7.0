{
    'name' : 'Changzhou Longcheng Yingcai Chuangye Investment Workflow Demo',
    'version' : '2.0',
    'author' : 'hp',
    'category' : 'workflow',
    'description' : """
    This is a workflow for longcheg yingcai.
    """,
    'website': 'http://www.openerp.com',
    'images' : [],
    'depends' : ['mail'],
    'data': [
             'security/investment_security.xml',
             'view/corp_view.xml',
             'view/region_view.xml',
             'view/investment_view.xml',
             'workflow/investment_workflow.xml',
             'view/commentline_view.xml',
             'view/enterprise_view.xml',
             'workflow/enterprise_workflow.xml',
             #'edi/mail_template.xml',
             'report/sqlreport_view.xml',
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
