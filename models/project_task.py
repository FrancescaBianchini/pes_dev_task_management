# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # Campo related al progetto, store=True per poter filtrare/raggruppare
    is_dev_project = fields.Boolean(
        related='project_id.is_dev_project',
        store=True,
        readonly=True,
        string='Is Dev Project',
    )

    is_epic = fields.Boolean(string='Is Epic')

    epic_id = fields.Many2one(
        comodel_name='project.task.epic',
        string='Epic',
        help="Epic di appartenenza del task.",
    )

    # default=0 sui campi Integer per evitare NULL in DB:
    # in PostgreSQL ORDER BY ... ASC mette i NULL in coda (NULLS LAST),
    # quindi senza default i record preesistenti rovinano l'ordinamento
    # della roadmap. Con default=0 Odoo:
    # - usa 0 come valore per i nuovi record
    # - backfilla a 0 le righe esistenti al momento della creazione della
    #   colonna (su installazioni fresche).
    # Per i database in cui il modulo era gia' installato senza default,
    # vedi anche migrations/17.0.5.0.1/post-migration.py
    release = fields.Integer(string='Release', default=0)
    sprint = fields.Integer(string='Sprint', default=0)
    us_code = fields.Char(string='US Code')
    estimate = fields.Integer(string='Estimate', default=0)

    value = fields.Selection(
        selection=[
            ('0', '0'),
            ('25', '25'),
            ('50', '50'),
            ('75', '75'),
            ('100', '100'),
        ],
        string='Value',
    )

    application_ids = fields.Many2many(
        comodel_name='project.application',
        relation='project_task_application_rel',
        column1='task_id',
        column2='application_id',
        string='Application',
    )

    acceptance_criteria = fields.Html(string='Acceptance Criteria', sanitize=False)
    dev_notes = fields.Html(string='Note', sanitize=False)

    @api.onchange('is_epic')
    def _onchange_is_epic(self):
        # Se il task diventa Epic, azzero il legame all'epic padre
        for rec in self:
            if rec.is_epic:
                rec.epic_id = False

