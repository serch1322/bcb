# -*- coding: utf-8 -*-

{
    'name': 'Buro de Credito Biometrico',
    'version': '1.0',
    'summary': 'Modulo de Buro de Credito Biometrico',
    'website': 'https://www.itreingenierias.com',
    'depends': [
        'base',
        'mail',
        'contacts',
        'website',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/bcb_usuario_final.xml',
        'views/res_partner.xml',
        'views/templates.xml',
        'wizard/revisar_foto.xml',
        'report/manifesto.xml',
        'data/website_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'bcb/static/src/js/usuario_final.js',
        ],
        'web.assets_qweb': [
            'portal/static/src/xml/portal_chatter.xml',
            'portal/static/src/xml/portal_signature.xml',
        ],
    },

}