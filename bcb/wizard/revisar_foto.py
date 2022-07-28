# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools
import cv2
import os
import base64

class RevisarFoto(models.TransientModel):
    _name = 'revisar.foto'

    foto = fields.Binary(string="Fotografía", required=True)

    def revisar_foto(self):
        imagen_cargada = cv2.imread('%s' %self.foto)
        imagen_cargada = cv2.imread(imagen_cargada)
        print(imagen_cargada)
        puntaje = 0
        usuarios = self.env['bcb.usuario.final'].search([])
        parecido = []
        for usuario in usuarios:
            imagen_rostro = cv2.imread('%s' %usuario.rostro)

            sift = cv2.SIFT_create()

            keypoints_1, descriptors_1 = sift.detectAndCompute(imagen_cargada, None)
            keypoints_2, descriptors_2 = sift.detectAndCompute(imagen_rostro, None)

            parecidos = cv2.FlannBasedMatcher({'algorithm':1, 'trees': 10},
                                       {}).knnMatch(descriptors_1, descriptors_2, k=1)

            puntos_parecido = []

            for p, q in parecidos:
                if p.distance < 0.1 * q.distance:
                    puntos_parecido.append(p)

            keypoints = 0
            if len(keypoints_1) < len(keypoints_2):
                keypoints = len(keypoints_1)
            else:
                keypoints = len(keypoints_2)

            if len(puntos_parecido) / keypoints * 100 > puntaje:
                puntaje = len(puntos_parecido) / keypoints * 100
                parecido.append(usuario)

            if len(parecido) <= 1:
                value = {
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'bcb.usuario.final',
                    'view_id': view_id,
                    'type': 'ir.actions.act_window',
                    'name': _('Usuario Final Bcb'),
                    'res_id': parecido and parecido[0]
                }
            else:
                value = {
                    'domain': str([('id', 'in', parecido)]),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'bcb.usuario.final',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'name': _('Usuario Final Bcb'),
                    'res_id': parecido
                }
            return value
