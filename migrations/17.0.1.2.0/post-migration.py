# -*- coding: utf-8 -*-
"""
Post-migration 17.0.1.2.0
Per ogni task che aveva un epic_id (riferimento a project.task con is_epic=True):
  1. Crea un record project.task.epic con nome, project_id e tag del vecchio task epic
  2. Aggiorna epic_id sul task con il nuovo ID

Ogni vecchio task-epic genera un unico project.task.epic.
"""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    cr.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = '_pes_epic_migration'
        )
    """)
    if not cr.fetchone()[0]:
        return

    cr.execute("SELECT COUNT(*) FROM _pes_epic_migration")
    if cr.fetchone()[0] == 0:
        cr.execute("DROP TABLE IF EXISTS _pes_epic_migration")
        return

    env = api.Environment(cr, SUPERUSER_ID, {})

    # Recupera gli ID distinti dei vecchi task-epic
    cr.execute("SELECT DISTINCT epic_task_id FROM _pes_epic_migration")
    old_epic_task_ids = [row[0] for row in cr.fetchall()]

    # Crea un project.task.epic per ogni vecchio task-epic
    epic_id_map = {}  # old project.task id → nuovo project.task.epic id
    for old_task in env['project.task'].browse(old_epic_task_ids):
        new_epic = env['project.task.epic'].create({
            'name': old_task.name,
            'project_id': old_task.project_id.id or False,
            'tag_ids': [(6, 0, old_task.tag_ids.ids)],
        })
        epic_id_map[old_task.id] = new_epic.id

    # Aggiorna epic_id sui task con i nuovi ID
    for old_epic_task_id, new_epic_id in epic_id_map.items():
        cr.execute("""
            UPDATE project_task
            SET epic_id = %s
            WHERE id IN (
                SELECT task_id
                FROM _pes_epic_migration
                WHERE epic_task_id = %s
            )
        """, (new_epic_id, old_epic_task_id))

    cr.execute("DROP TABLE IF EXISTS _pes_epic_migration")
