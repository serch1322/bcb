# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools
from PIL import Image

##OCR de INE para que usuario no tenga que capturar datos de cliente

class BcbUsuarioFinal(models.Model):
    _name = 'bcb.usuario.final'
    _description = 'Usuario Final'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # ------------------Información Cliente---------------------------
    name = fields.Char(string='Usuario', readonly=True)
    nombre = fields.Char(string='Nombre', required=True, tracking=True)
    apellido_paterno = fields.Char(string='Apellido Paterno', required=True, tracking=True)
    apellido_materno = fields.Char(string='Apellido Materno', required=True, tracking=True)
    curp = fields.Char(string="Curp")
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento")
    pais = fields.Many2one('res.country', string="País", tracking=True)
    estado = fields.Many2one('res.country.state', string="Estado", tracking=True)
    municipio = fields.Char(string="Ciudad", tracking=True)
    colonia = fields.Char(string="Colonia", tracking=True)
    cp = fields.Char(string="Código Postal", tracking=True)
    ##Revisar como poner lada del país en el celular
    celular = fields.Char(string="Celular", tracking=True)
    ##Revisar como pedir que se complete email
    email = fields.Char(string="Correo Electronico", tracking=True)
    #------------------Documentos Legales---------------------------
    nombre_manuscrito = fields.Binary(string="Nombre Manuscrito")
    firma = fields.Binary(string="Firma")
    contrato = fields.Binary(string="Contrato Firmado", attachment=True)
    ##Ajustar Fecha para solo revisar año de INE
    vigencia_ine = fields.Date(string="Vigencia de INE", tracking=True)
    ine_frontal = fields.Image(string='Ine Frontal', required=True, attachment=True, max_width=1024, max_height=1024)
    ine_posterior = fields.Image(string='Ine Posterior', required=True, attachment=True, max_width=1024, max_height=1024)
    rostro = fields.Image(string='Rostro', required=True, attachment=True, max_width=1024, max_height=1024)
    state = fields.Selection([('limpio', 'Limpio'),('moroso', 'Moroso'),('fraude', 'Fraude')], 'Estado', default='limpio', index=True, store=True, required=True, readonly=False, tracking=True)
    huellas_dactilares = fields.One2many('huella.dactilar', 'usuario_id', string="Huella Dactilar")
    empresas = fields.One2many('empresa.usuario', 'usuario_id', string="Empresas")
    ##Mostrar cuantos usuarios finales estan ligados a la empresa
    clientes = fields.Many2many('res.partner', domain=[('parent_id','=',False)])
    ##Fraude de Datos
    ##Revisión de Foto de INE con Rostro
    ##Agregar una notificación que el usuario fue cambiado a fraude


    @api.onchange('nombre', 'apellido_paterno', 'apellido_materno')
    def cambiar_nombre(self):
        if self.nombre and self.apellido_paterno and self.apellido_materno:
            self.name = '%s %s %s' %(self.nombre,self.apellido_paterno,self.apellido_materno)
        else:
            None

    def estado_limpio(self):
        self.state = 'limpio'

    def estado_moroso(self):
        self.state = 'moroso'

    def estado_fraude(self):
        self.state = 'fraude'

    def revisar_foto(self):
        None

    def revisar_cara(self):
        None


class HuellaDactilar(models.Model):
    _name = 'huella.dactilar'
    _description = 'Huello Dactilar'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    usuario_id = fields.Many2one('bcb.usuario.final',string="Huellas de")
    huella_dactilar = fields.Image(string="Huella Dactilar", required=True)
    mano = fields.Selection([('derecha', 'Derecha'),('izquierda', 'Izquierda')], 'Mano', store=True, required=True)

class EmpresaUsuario(models.Model):
    _name = 'empresa.usuario'
    _description = 'Empresa Usuario'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Empresa", store=True, required=True)
    usuario_id = fields.Many2one('bcb.usuario.final',string="Usuario")
    cliente = fields.Many2one('res.user', string="Usuario", default=lambda self:self.env.user, readonly=True)
    #Poner RFC en revisión
    rfc = fields.Char(string="RFC", store=True, required=True)
    evidencia = fields.Binary(string="Evidencia", attachment=True, readonly=True)
    state = fields.Selection([('limpio', 'Limpio'),('moroso', 'Moroso'),('fraude', 'Fraude')], 'Estado', default='limpio', index=True, store=True, required=True, readonly=False, tracking=True)
    #Poner documentos que cargue la persona que validen lo esta fraudeando.

    def actualizar_state(self):
        None

    # Realizar Creación de Empresa Nueva
    def _crear_empresa(self, usuario_id=None, name=None, rfc=None, **kw):
        """ Crear Empresa Nueva dentro de Usuario Final """
        self.ensure_one()
        emp_obj = self.env['empresa.usuario']
        valores_empresa = {}
        valores_empresa.update({
            'name': name,
            'usuario_id': usuario_id,
            'cliente': lambda self: self.env.user,
            'rfc': rfc,
            'state': 'limpio'
        })
        empresa_creada = emp_obj.create(valores_empresa)