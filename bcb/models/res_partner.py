# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    cuenta_usuario_bcb = fields.Integer(compute='_compute_usuario_bcb', string='Cuenta de Usuarios BCB')
    bcb_ids = fields.One2many('bcb.usuario.final', 'clientes', 'Usuario BCB')

    def _compute_usuario_bcb(self):
        None
    #     # retrieve all children partners and prefetch 'parent_id' on them
    #     all_partners = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
    #     all_partners.read(['parent_id'])
    #
    #     grupos_bcb = self.env['bcb.usuario.final'].read_group(
    #         domain=[('clientes', 'in', all_partners.ids)],
    #         fields=['clientes'], groupby=['clientes']
    #     )
    #     partners = self.browse()
    #     for group in grupos_bcb:
    #         partner = self.browse(group['partner_id'][0])
    #         while partner:
    #             if partner in self:
    #                 partner.cuenta_usuario_bcb += group['partner_id_count']
    #                 partners |= partner
    #             partner = partner.parent_id
    #     (self - partners).cuenta_usuario_bcb = 0

    def ver_bcb(self):
        None
        # action = self.env['ir.actions.act_window']._for_xml_id('bcb.res_partner_bcb')
        # if self.is_company:
        #     action['domain'] = [('clientes.commercial_partner_id.id', '=', self.id)]
        # else:
        #     action['domain'] = [('clientes.id', '=', self.id)]
        # return action