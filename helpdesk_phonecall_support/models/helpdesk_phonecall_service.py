# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import UserError


class HelpDeskPhoneCallService(models.Model):
    _name = 'helpdesk.phonecall.service'
    _rec_name = 'title'

    title = fields.Char(string='Title')

    description = fields.Text(string='Description')

    start_date_hour = fields.Datetime(string='Start Date',
                                      copy=False,
                                      readonly=True,
                                      change_default=True,
                                      store=True,
                                      default=lambda x: fields.datetime.now())

    partner_id = fields.Many2one(string='Partner',
                                 required=True,
                                 comodel_name='res.partner')

    project_id = fields.Many2one(string='Project',
                                 required=True,
                                 comodel_name='project.project')

    contact_partner_id = fields.Many2one(string='Contact',
                                         required=True,
                                         comodel_name='res.partner')

    user_id = fields.Many2one('res.users',
                              string='User',
                              readonly=True,
                              copy=False,
                              default=lambda self: self._uid)

    finish_date_hour = fields.Datetime(string='Finish Date',
                                       copy=False,
                                       readonly=True, )

    phonecall_tag_id = fields.Many2one('helpdesk.phonecall.service.tag',
                                       string='Tags')

    external_code = fields.Char(string='External Code',
                                readonly=True,
                                copy=False)

    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 readonly=True,
                                 states={
                                     'done': [('readonly', False)],
                                 },
                                 default=lambda self: self.env.user.company_id)

    state = fields.Selection(string='State', readonly=True,
                             selection=[
                                 ('open', 'Open'),
                                 ('done', 'Done'),
                             ],
                             copy=False,
                             default='open')

    active = fields.Boolean(default=True)

    @api.onchange('start_date_hour', 'partner_id', 'project_id')
    def _onchange_title(self):
        for rec in self:
            rec.title = ''
            rec.title += rec.start_date_hour if rec.start_date_hour else ''
            rec.title += ', ' + rec.partner_id.name if rec.partner_id else ''
            rec.title += ', ' + rec.project_id.name if rec.project_id else ''

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if not self.partner_id.is_company:
            self.contact_partner_id = self.partner_id
        else:
            self.contact_partner_id = False

    @api.multi
    def action_finish_phonecall(self):
        self.ensure_one()
        if (not self.phonecall_tag_id) or (not self.description):
            raise UserError(_('Please make sure the marker or '
                              'description fields are filled in.'))

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.phonecall.confirm',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(False, "form")],
            'target': 'new',
        }

    @api.model
    def create(self, values):
        # Quando salvamos a criação do atendimento, o sistema esta recalculando
        # a data de início (criação) para data de salvamento.
        # Este método faz com que o sistema pegue novamente a data de criação
        # armazenada no campo title e sobrescreva no campo.
        values['start_date_hour'] = values['title'].split(',')[0]
        return super(HelpDeskPhoneCallService, self).create(values)
