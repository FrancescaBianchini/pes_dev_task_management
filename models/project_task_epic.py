# -*- coding: utf-8 -*-
from odoo import fields, models


class ProjectTaskEpic(models.Model):
    _name = 'project.task.epic'
    _description = 'Epic'
    _order = 'name'

    name = fields.Char(string='Name', required=True)

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        ondelete='cascade',
    )

    tag_ids = fields.Many2many(
        comodel_name='project.tags',
        relation='project_task_epic_tags_rel',
        column1='epic_id',
        column2='tag_id',
        string='Labels',
    )

    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='epic_id',
        string='Tasks',
    )
