# -*- coding: utf-8 -*-
"""
Pre-migration 17.0.1.2.0
Salva la mappatura task_id → epic_task_id prima che Odoo modifichi la colonna
epic_id (il comodel cambia da project.task a project.task.epic).
Azzera epic_id per evitare violazioni di FK durante l'aggiornamento.
"""


def migrate(cr, version):
    cr.execute("""
        CREATE TABLE IF NOT EXISTS _pes_epic_migration (
            task_id     INTEGER NOT NULL,
            epic_task_id INTEGER NOT NULL
        )
    """)
    cr.execute("""
        INSERT INTO _pes_epic_migration (task_id, epic_task_id)
        SELECT id, epic_id
        FROM project_task
        WHERE epic_id IS NOT NULL
    """)
    # Azzera la colonna per evitare FK constraint violations quando
    # Odoo ricrea il vincolo verso project_task_epic
    cr.execute("UPDATE project_task SET epic_id = NULL WHERE epic_id IS NOT NULL")
