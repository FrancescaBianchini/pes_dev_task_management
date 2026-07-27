/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { onMounted, onWillUnmount } from "@odoo/owl";

const PARAM_KEY = "pes_dev_task_management.task_auto_refresh_interval";
const DEFAULT_INTERVAL_S = 30;

// Promessa condivisa: la chiamata RPC per leggere il parametro viene eseguita
// una sola volta per sessione, indipendentemente da quante viste si aprono.
let _intervalMsPromise = null;

function fetchIntervalMs(orm) {
    if (!_intervalMsPromise) {
        _intervalMsPromise = orm
            .call("ir.config_parameter", "get_param", [PARAM_KEY, String(DEFAULT_INTERVAL_S)])
            .then((val) => Math.max(5, parseInt(val) || DEFAULT_INTERVAL_S) * 1000)
            .catch(() => DEFAULT_INTERVAL_S * 1000);
    }
    return _intervalMsPromise;
}

function patchAutoRefresh(Controller) {
    patch(Controller.prototype, {
        setup() {
            super.setup(...arguments);

            const context = this.props.context || {};
            if (!context.task_auto_refresh) {
                return;
            }

            const orm = useService("orm");
            let timer = null;
            let loading = false;

            onMounted(async () => {
                let intervalMs;
                if (context.task_auto_refresh_interval) {
                    intervalMs = Math.max(5, context.task_auto_refresh_interval) * 1000;
                } else {
                    intervalMs = await fetchIntervalMs(orm);
                }

                timer = setInterval(() => {
                    if (loading) {
                        return;
                    }
                    loading = true;
                    this.model
                        .load()
                        .catch(() => {})
                        .finally(() => {
                            loading = false;
                        });
                }, intervalMs);
            });

            onWillUnmount(() => {
                if (timer) {
                    clearInterval(timer);
                    timer = null;
                }
            });
        },
    });
}

patchAutoRefresh(ListController);
patchAutoRefresh(KanbanController);
