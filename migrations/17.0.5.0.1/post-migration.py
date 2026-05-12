# -*- coding: utf-8 -*-
"""
Migrazione 17.0.5.0.1 - Fix ordinamento NULL.

Le versioni precedenti del modulo dichiaravano i campi release / sprint /
estimate come fields.Integer senza default=0. Quando le colonne sono state
aggiunte alla tabella project_task tramite ALTER TABLE, i record gia'
esistenti hanno ricevuto NULL invece di 0.

Questo script SQL backfilla i NULL a 0 cosi' l'ordinamento ASC della
vista Roadmap mostra correttamente i task "non assegnati" (value=0)
in cima alla lista (Postgres ordina i NULL LAST in ASC).

Lo script viene eseguito automaticamente da Odoo all'upgrade del modulo
verso la versione 17.0.5.0.1 (post-phase: dopo il caricamento del nuovo
codice del modulo).
"""


def migrate(cr, version):
    if not version:
        # Fresh install: l'_init_column di Odoo gestisce gia' i default
        # grazie al default=0 ora dichiarato sui campi; nulla da fare.
        return

    cr.execute(
        """
        UPDATE project_task
        SET release = 0
        WHERE release IS NULL
        """
    )
    cr.execute(
        """
        UPDATE project_task
        SET sprint = 0
        WHERE sprint IS NULL
        """
    )
    cr.execute(
        """
        UPDATE project_task
        SET estimate = 0
        WHERE estimate IS NULL
        """
    )
