# PES Dev Task Management

**Version:** 17.0.1.0.0
**Author:** Progetti & Soluzioni
**License:** LGPL-3

## Descrizione

Modulo Odoo 17 che estende la gestione progetti standard per supportare workflow di sviluppo software agile/Scrum. Aggiunge campi e viste specializzati per gestire **Epic**, **User Story**, **Release**, **Sprint** e **Applicazioni**, attivabili singolarmente su ogni progetto tramite un flag dedicato.

---

## Funzionalità

### Flag di progetto 

Nelle impostazioni di ogni progetto compare il campo **Is Dev Project**. Finché non è abilitato, nessun campo di sviluppo è visibile sui task — i progetti non-dev restano invariati.

---

### Modello: Application

Nuovo modello per gestire le applicazioni/sistemi coinvolti nei task.

| Campo | Tipo | Descrizione |
|---|---|---|
| `name` | Char | Nome applicazione (univoco) |
| `color` | Integer | Colore del badge |
| `active` | Boolean | Archiviazione soft |

Le applicazioni si gestiscono da **Configurazione → Applicazioni** e sono accessibili ai Project Manager in CRUD e agli utenti in sola lettura.

---

### Campi aggiuntivi su `project.task`

Visibili solo se il progetto ha `is_dev_project = True`.

| Campo | Tipo | Descrizione |
|---|---|---|
| `is_epic` | Boolean | Segna il task come Epic |
| `epic_id` | Many2one | Epic padre (stesso progetto) |
| `release` | Integer | Numero di release |
| `sprint` | Integer | Numero di sprint |
| `us_code` | Char | Codice User Story (es. "US-001") |
| `estimate` | Integer | Stima (story points / ore) |
| `value` | Selection | Valore/priorità: 0, 25, 50, 75, 100 |
| `application_ids` | Many2many | Applicazioni coinvolte (tag colorati) |
| `acceptance_criteria` | Html | Criteri di accettazione (Definition of Done) |
| `dev_notes` | Html | Note tecniche interne |

**Logica business:**
- Segnare un task come Epic svuota automaticamente il campo `epic_id` (nessun Epic dentro un Epic).
- Cambiare progetto su un task svuota `epic_id` se l'Epic appartiene al progetto precedente.
- I campi interi (`release`, `sprint`, `estimate`) hanno default `0` anziché NULL per garantire un ordinamento corretto nella vista Roadmap.

---

### Viste

#### Form
- Gruppo campi dev (due colonne) visibile solo su progetti dev.
- Tab **Acceptance Criteria** e **Note** con editor HTML.

#### Lista (Tree)
- Multi-edit abilitato: seleziona più righe e modifica in blocco release, sprint, stima, ecc.
- Colonne aggiuntive opzionali: Epic, Release, Sprint, US Code, Estimate, Value, Deadline.

#### Kanban
- Badge colorati nelle card: US Code (blu), Release ("R{n}"), Sprint ("S{n}").

#### Ricerca
- Filtri rapidi: **Is Epic / Is not Epic**, **With/Without Release**, **With/Without Sprint**.
- Group by: Value, Release, Sprint, US Code, Application.

---

### Menu e accesso rapido

| Voce | Posizione | Descrizione |
|---|---|---|
| Dev Tasks | Progetto (seq. 15) | Task filtrati per `is_dev_task = True` |
| Applicazioni | Progetto → Configurazione | CRUD applicazioni |

**Filtro Roadmap** (predefinito su Dev Tasks):
Ordine automatico → Release → Sprint → Deadline → US Code.

---

### Sicurezza

| Gruppo | Application |
|---|---|
| Project User | Read |
| Project Manager | Read, Write, Create, Delete |

---

## Installazione

Il modulo è compatibile con **Odoo 17.0**. Non richiede dipendenze esterne oltre al modulo `project`.

```
'depends': ['project']
```

---

## Note di migrazione

Dalla versione `17.0.5.0.1` è presente uno script di post-migrazione che aggiorna a `0` i valori NULL sui campi `release`, `sprint` ed `estimate` nelle installazioni esistenti.
