{
    'name': 'PES Dev Task Management',
    'version': '17.0.1.2.0',
    'category': 'Project',
    'summary': 'Gestione task di sviluppo: Epic, Release, Sprint, US Code, etc.',
    'description': """
Modulo per la gestione dei task di sviluppo software in Odoo.
Aggiunge campi specifici al modello project.project e project.task:
- Flag is_dev_project sul progetto
- Gestione Epic / User Story / Release / Sprint
- Applicazioni come tag many2many
- Acceptance Criteria e Note in HTML
- Vista list Roadmap come preferito condiviso
""",
    'author': 'Progetti & Soluzioni',
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_application_views.xml',
        'views/project_project_views.xml',
        'views/project_task_epic_views.xml',
        'views/project_task_views.xml',
        'views/project_task_action_dev.xml',
        'data/ir_filters_data.xml',
        'data/ir_config_parameter.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pes_dev_task_management/static/src/js/task_auto_refresh.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
