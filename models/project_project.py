# -*- coding: utf-8 -*-
from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    is_dev_project = fields.Boolean(
        string='Is Dev Project',
        default=False,
        help="Se attivo, abilita i campi specifici di gestione sviluppo "
             "(Epic, Release, Sprint, US Code, ecc.) sui task del progetto."
    )
