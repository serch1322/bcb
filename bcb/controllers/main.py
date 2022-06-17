# -*- coding: utf-8 -*-

from odoo import http
import base64
import cv2
import numpy as np
from odoo.addons.http_routing.models.ir_http import slug

class BCBWeb(http.Controller):

    #Validación de Datos
    @http.route('/validar_datos', auth="public", website=True )
    def validar_datos(self, **kw):
        return http.request.render('bcb.validar_datos')
        # imagen_cargada = http.request.params.get('imagen','')
        # #imagen_cargada = base64.encodebytes(imagen_cargada.read())
        # puntaje = 0
        # usuarios = http.request.env['bcb.usuario.final'].search([])
        # parecido = []
        # for usuario in usuarios:
        #     imagen_rostro = cv2.imread('%s' % usuario.rostro)
        #     sift = cv2.SIFT_create()
        #
        #     keypoints_1, descriptors_1 = sift.detectAndCompute(imagen_cargada, None)
        #     keypoints_2, descriptors_2 = sift.detectAndCompute(imagen_rostro, None)
        #
        #     parecidos = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10},
        #                                       {}).knnMatch(descriptors_1, descriptors_2, k=1)
        #
        #     puntos_parecido = []
        #
        #     for p, q in parecidos:
        #         if p.distance < 0.1 * q.distance:
        #             puntos_parecido.append(p)
        #
        #     keypoints = 0
        #     if len(keypoints_1) < len(keypoints_2):
        #         keypoints = len(keypoints_1)
        #     else:
        #         keypoints = len(keypoints_2)
        #
        #     if len(puntos_parecido) / keypoints * 100 > puntaje:
        #         puntaje = len(puntos_parecido) / keypoints * 100
        #         parecido.append(usuario)
        #
        #     if len(parecido) <= 1:
        #         value = {
        #             'view_type': 'form',
        #             'view_mode': 'form',
        #             'res_model': 'bcb.usuario.final',
        #             'view_id': view_id,
        #             'type': 'ir.actions.act_window',
        #             'name': _('Usuario Final Bcb'),
        #             'res_id': parecido and parecido[0]
        #         }
        #     else:
        #         value = {
        #             'domain': str([('id', 'in', parecido)]),
        #             'view_type': 'form',
        #             'view_mode': 'tree,form',
        #             'res_model': 'bcb.usuario.final',
        #             'view_id': False,
        #             'type': 'ir.actions.act_window',
        #             'name': _('Usuario Final Bcb'),
        #             'res_id': parecido
        #         }
        #     return value
        # return http.request.render('bcb.validar_datos')

    # Busqueda Usuario Final
    @http.route(['/listado_clientes', '/listado_clientes/pagina/<int:page>'], type='http', auth="user", website=True)
    def listado_clientes (self, page=0, **kw):
        domain = []
        usuario = http.request.env['bcb.usuario.final']

        #Usando la buscador
        busqueda = http.request.params.get('search', '' )
        if busqueda:
            domain.append( ('name', 'ilike',busqueda.strip() ))


        search_usuario = usuario.search(domain)
        ppg=9
        pager = http.request.website.pager(
            url= '/listado_clientes',
            total= len(search_usuario),
            page = page, #Pagina actual
            step= ppg, #Item por pagina
            scope= 3, #Numero de paginas a mostrar
            url_args=kw
        )
        #_logger.error('PAGINACION: %s', pager)
        offset = pager['offset']
        usuarios = search_usuario[offset:offset+ppg]

        #currency = http.request.env.company.currency_id

        return http.request.render('bcb.listado_clientes',{
            'usuarios': usuarios,
            'pager': pager,
            'busqueda': busqueda,
        })

    #Vista Usuario Final
    @http.route('/usuario_final/<model("bcb.usuario.final"):usuario>/', auth="user",website=True)
    def show_producto_model(self, usuario, **kw):
        return http.request.render('bcb.usuario_final', {'usuario': usuario})

    #Crear Empresa para Usuario Final
    @http.route('/crearempresa/<model("bcb.usuario.final"):usuario>', auth="user", website=True)
    def crearEmpresa(self, usuario=None, **kw):
        usuario_final = http.request.env['bcb.usuario.final'].browse(int(http.request.params.get('usuario_id', False)))
        if usuario_final:
            http.request.env['empresa.usuario'].create({
                'usuario_id': self.usuario_final,
                'cliente': http.request.params.get('cliente', ''),
                'empresa': http.request.params.get('empresa', ''),
                'rfc': http.request.params.get('rfc', ''),
            })
            return http.request.redirect('/usuario_final/' + str(usuario_final.id))
        return http.request.render('bcb.crear_empresa', {'usuario_final': usuario})