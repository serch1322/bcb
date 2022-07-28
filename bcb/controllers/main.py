# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.addons.portal.controllers.portal import pager as portal_pager
from collections import OrderedDict
from odoo.osv.expression import OR, AND
from markupsafe import Markup
import base64
import cv2
import numpy as np
from odoo.addons.http_routing.models.ir_http import slug
import  logging
_logger = logging.getLogger(__name__)

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

    #Valores para Buscar
    def _valores_para_buscador_usuario(self):
        values = {
            'all': {'input': 'all', 'label': ('Buscar en Todo'), 'order': 1},
            'name': {'input': 'name', 'label': _('Buscar por Nombre'), 'order': 2},
            'estado': {'input': 'estado', 'label': _('Buscar por Estado'), 'order': 3},
        }
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))

    #Buscador por Dominio
    def _buscar_usuario_por_filtro(self, search_in, search):
        search_domain = []
        if search_in in ('all', 'all'):
            search_domain.append([('name', 'ilike', search)])
            search_domain.append([('state', 'ilike', search)])
        if search_in in ('name', 'all'):
            search_domain.append([('name', 'ilike', search)])
        if search_in in ('estado', 'all'):
            search_domain.append([('state', 'ilike', search)])
        return search_domain

    #Acomodar por Busqueda
    def _acomodar_por_usuario(self):
        return {
            'create_desc': {'label': _('Más Reciente a Más Antiguo'), 'order': 'create_date desc', 'sequence': 1},
            'create_asc': {'label': _('Más Antiguo a Más Reciente'), 'order': 'create_date asc', 'sequence': 2},
            'name_asc': {'label': _('Nombre A-Z'), 'order': 'name asc', 'sequence': 3},
            'name_desc': {'label': _('Nombre Z-A'), 'order': 'name desc', 'sequence': 4},
        }

    ## Arreglar buscador y arreglar acomodador

    # Busqueda Usuario Final
    @http.route(['/listado_clientes', '/listado_clientes/pagina/<int:page>'], type='http', auth="user", website=True)
    def listado_clientes (self, page=1, sortby=None, filterby=None, search=None, search_in='all', **kw):
        domain = []
        usuario = http.request.env['bcb.usuario.final']

        searchbar_inputs = self._valores_para_buscador_usuario()

        if search and search_in:
            domain += self._buscar_usuario_por_filtro(search_in, search)

        searchbar_filters = {
            'todos': {'label': _('Todos'), 'domain': []},
            'limpio': {'label': _('Limpio'), 'domain': [('state', '=', 'limpio')]},
            'moroso': {'label': _('Moroso'), 'domain': [('state', '=', 'moroso')]},
            'fraude': {'label': _('Fraude'), 'domain': [('state', '=', 'fraude')]},
        }

        searchbar_sortings = self._acomodar_por_usuario()
        searchbar_sortings = dict(sorted(self._acomodar_por_usuario().items(),
                                         key=lambda item: item[1]["sequence"]))

        # Orden por usuarios predeterminado
        if not sortby:
            sortby = 'create_desc'
        usuarios = searchbar_sortings[sortby]['order']

        # Valor de filtro predeterminado
        if not filterby:
            filterby = 'todos'
        domain += searchbar_filters[filterby]['domain']


        search_usuario = usuario.search(domain)
        ppg=9
        pager = portal_pager(
            url= '/listado_clientes',
            total= len(search_usuario),
            page = page, #Pagina actual
            step= ppg, #Item por pagina
            scope= 3, #Numero de paginas a mostrar
            url_args={'sortby': sortby},
        )
        offset = pager['offset']
        usuarios = search_usuario[offset:offset+ppg]

        return http.request.render('bcb.listado_clientes',{
            'usuarios': usuarios,
            'pager': pager,
            'default_url': '/listado_clientes',
            'searchbar_inputs': searchbar_inputs,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'search': search,
        })

    #Vista Usuario Final
    @http.route('/usuario_final/<model("bcb.usuario.final"):usuario>/', auth="user",website=True)
    def show_producto_model(self, usuario, **kw):
        return http.request.render('bcb.usuario_final', {'usuario': usuario})

    # #Crear Empresa para Usuario Final
    # @http.route('/crearempresa/<model("bcb.usuario.final"):usuario>', auth="user", website=True)
    # def crearEmpresa(self, usuario=None, **kw):
    #     usuario_final = http.request.env['bcb.usuario.final'].browse(int(http.request.params.get('usuario_id', False)))
    #     if usuario_final:
    #         http.request.env['empresa.usuario'].create({
    #             'usuario_id': self.usuario_final,
    #             'cliente': http.request.params.get('cliente', ''),
    #             'empresa': http.request.params.get('empresa', ''),
    #             'rfc': http.request.params.get('rfc', ''),
    #         })
    #         return http.request.redirect('/usuario_final/' + str(usuario_final.id))
    #     return http.request.render('bcb.crear_empresa', {'usuario_final': usuario})

    @http.route(['/crear_empresa'], type='json', methods=['POST'], auth="user", website=True, csrf=False)
    def crear_empresa(self, **kw):
        usuario_final = http.request.env['empresa.usuario'].create({
            'usuario_id': int(http.request.params.get('usuario_id', False)),
            'name': str(http.request.params.get('name', False)),
            'rfc': str(http.request.params.get('rfc', False)),
            'state': 'limpio',
            'cliente': http.request.env.user.id,
        })
        _logger.error('Usuario_Final: %s', usuario_final)

        return 'Ok'