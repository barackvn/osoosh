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

odoo.define("prt_mail_messages_pro/static/src/models/messaging_notification_handler/messaging_notification_handler.js", function (require) {
    "use strict";

    const { registerInstancePatchModel } = require("mail/static/src/model/model_core.js");

    registerInstancePatchModel("mail.messaging_notification_handler", "prt_mail_messages_pro/static/src/models/messaging_notification_handler/messaging_notification_handler.js", {
        async _handleNotificationPartner(data) {
            const { type } = data;
            if (type === "filter_updated") {
                return await this._handleNotificationThreadFilter(data);
            } else if(type === "message_updated") {
                return await this._handleNotificationMessage(data);
            } else {
                return this._super(data);
            }
        },
        async _handleNotificationThreadFilter({ filter, value, thread_id, thread_model }) {
            // update thread filters
            const thread = this.env.models["mail.thread"].find(thread =>
                thread.id === thread_id &&
                thread.model === thread_model
            );
            if (thread) {
                if (filter === "hide_notifications") {
                    thread.update({
                        "displayNotifications": !value,
                    });
                } else if (filter === "hide_notes") {
                    thread.update({
                        "displayNotes": !value,
                    });
                } else if (filter === "hide_messages") {
                    thread.update({
                        "displayMessages": !value,
                    });
                }
                await thread.applyThreadFilters();
            }
        },
        async _handleNotificationMessage({ message_ids, action }) {
            for (const msg of message_ids) {
                const message = this.env.models["mail.message"].find(message => message.id === msg.message_id);
                if (message) {
                    if (action === "move") {
                        // original thread
                        const originalThreadData = msg.originalThread;
                        const originalThread = this.env.models["mail.thread"].find(thread =>
                            thread.id === originalThreadData.thread_id && thread.model === originalThreadData.thread_model
                        );
                        // delete the message from original thread
                        originalThread.mainCache.update({ messages: [["unlink", message]] });
                        // moved thread
                        const movedThreadData = msg.movedThread;
                        const movedThread = this.env.models["mail.thread"].find(thread =>
                            thread.id === movedThreadData.thread_id && thread.model === movedThreadData.thread_model
                        );
                        // add the message to moved thread
                        movedThread.mainCache.update({ messages: [["link", message]] });
                    } else if (action === "edit") {
                        const fields = ["body", "cx_edit_message"]
                        const [ data ] = await this.async(() => this.env.services.rpc({
                            model: "mail.message",
                            method: "read",
                            args: [[message.id], fields],
                        }));
                        message.update({
                            "body": data.body,
                            "_cx_edit_message": data.cx_edit_message,
                        });
                    }
                }
            }
        },
    });
});
