# -*- coding: utf-8 -*-
from odoo import fields, models


class ProjectApplication(models.Model):
    _name = 'project.application'
    _description = 'Project Application'
    _order = 'name'

    name = fields.Char(string='Application', required=True, translate=True)
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Application name must be unique!'),
    ]
