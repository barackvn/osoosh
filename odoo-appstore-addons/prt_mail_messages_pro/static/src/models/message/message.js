/**********************************************************************************
* 
*    Copyright (C) 2020 Cetmix OÜ
*
*   Odoo Proprietary License v1.0
* 
*   This software and associated files (the "Software") may only be used (executed,
*   modified, executed after modifications) if you have purchased a valid license
*   from the authors, typically via Odoo Apps, or if you have received a written
*   agreement from the authors of the Software (see the COPYRIGHT file).
* 
*   You may develop Odoo modules that use the Software as a library (typically
*   by depending on it, importing it and using its resources), but without copying
*   any source code or material from the Software. You may distribute those
*   modules under the license of your choice, provided that this license is
*   compatible with the terms of the Odoo Proprietary License (For example:
*   LGPL, MIT, or proprietary licenses similar to this one).
* 
*   It is forbidden to publish, distribute, sublicense, or sell copies of the Software
*   or modified copies of the Software.
* 
*   The above copyright notice and this permission notice must be included in all
*   copies or substantial portions of the Software.
* 
*   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
*   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
*   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
*   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
*   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
*   ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
*   DEALINGS IN THE SOFTWARE.
*
**********************************************************************************/

odoo.define("prt_mail_messages_pro/static/src/models/message/message.js", function (require) {
    "use strict";

    const { registerInstancePatchModel, registerFieldPatchModel, registerClassPatchModel } = require("mail/static/src/model/model_core.js");
    const { attr } = require("mail/static/src/model/model_field.js");
    const Dialog = require("web.Dialog");

    registerClassPatchModel("mail.message", "prt_mail_messages_pro/static/src/models/message/message.js", {
        convertData(data) {
            const data2 = this._super(data);
            if ("cx_edit_message" in data) {
                data2._cx_edit_message = data.cx_edit_message;
            }
            return data2;
        },
    });

    registerInstancePatchModel("mail.message", "prt_mail_messages_pro/static/src/models/message/message.js", {
        replyQuote() {
            return this.openReplyAction("quote");
        },
        replyForward() {
            return this.openReplyAction("forward");
        },
        toMove() {
            return this.openMoveAction();
        },
        async toDelete() {
            await this._askDeleteConfirmation();
            await this.async(() => this.env.services.rpc({
                model: "mail.message",
                method: "unlink",
                args: [[this.id]],
            }));
        },
        toEdit() {
            this.openEditAction();
        },
        async openReplyAction(mode) {
            const context = await this.async(() => this.env.services.rpc({
                model: "mail.message",
                method: "reply_prep_context",
                args: [[this.id]],
                kwargs: {
                    context: {
                        wizard_mode: mode,
                    },
                },
            }));
            const action = {
                type: "ir.actions.act_window",
                res_model: "mail.compose.message",
                view_mode: "form",
                views: [[false, "form"]],
                target: "new",
                context: context,
            };
            return this.env.bus.trigger("do-action", {
                action: action,
                options: {
                    on_close: () => {
                        this.originThread.refresh();
                    },
                },
            });
        },
        openMoveAction() {
            const thread = this.threads.find(thread => thread.model === "mail.channel")
            const action = {
                type: "ir.actions.act_window",
                res_model: "prt.message.move.wiz",
                view_mode: "form",
                views: [[false, "form"]],
                target: "new",
                context: {
                    thread_message_id: this.id,
                    old_thread_id: thread && thread.id || null,
                },
            };
            return this.env.bus.trigger("do-action", {action: action});
        },
        openEditAction() {
            const thread = this.threads.find(thread => thread.model === "mail.channel")
            const action = {
                type: "ir.actions.act_window",
                res_model: "cx.message.edit.wiz",
                view_mode: "form",
                views: [[false, "form"]],
                target: "new",
                context: {
                    message_edit_id: this.id,
                },
            };
            return this.env.bus.trigger("do-action", {action: action});
        },
        _askDeleteConfirmation() {
            return new Promise(resolve => {
                Dialog.confirm(this, this.env._t("Message will be deleted! Are you sure you want to delete?"), {
                    buttons: [
                        {
                            text: this.env._t("Delete"),
                            classes: "btn-primary",
                            close: true,
                            click: resolve,
                        },
                        {
                            text: this.env._t("Discard"),
                            close: true,
                        }
                    ]
                });
            });
        },
    });

    registerFieldPatchModel("mail.message", "prt_mail_messages_pro/static/src/models/message/message.js", {
        _cx_edit_message: attr(),
    });
});
