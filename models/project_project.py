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

    def action_view_tasks(self):
        action = super().action_view_tasks()
        if self.is_dev_project:
            ctx = action.get('context', {})
            if isinstance(ctx, str):
                try:
                    import ast
                    ctx = ast.literal_eval(ctx)
                except (ValueError, SyntaxError):
                    ctx = {}
            interval = int(self.env['ir.config_parameter'].sudo().get_param(
                'pes_dev_task_management.task_auto_refresh_interval', 30
            ))
            ctx['task_auto_refresh'] = True
            ctx['task_auto_refresh_interval'] = interval
            action['context'] = ctx
        return action
