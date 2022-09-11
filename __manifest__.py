# -*- coding: utf-8 -*-
{
    'name': "Trip_Request",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr','mail','hr_contract'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/auto_update_status.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/TripRequest.xml',
        'views/itqan_hr_employee.xml',
        'reports/trip_requests_report.xml',
        'reports/custom_header_footer_report.xml',
        'reports/trip_requests_template_report.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
