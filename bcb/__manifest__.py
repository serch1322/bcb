# -*- coding: utf-8 -*-

{
    'name': 'Buro de Credito Biometrico',
    'version': '1.0',
    'summary': 'Modulo de Buro de Credito Biometrico',
    'website': 'https://www.itreingenierias.com',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/bcb_usuario_final.xml',
        'views/templates.xml',
        'wizard/revisar_foto.xml',
        'report/manifesto.xml',
        'data/website_data.xml',
    ],
    'depends': [
        'base',
        'mail',
        'contacts',
        'website',
    ],
}