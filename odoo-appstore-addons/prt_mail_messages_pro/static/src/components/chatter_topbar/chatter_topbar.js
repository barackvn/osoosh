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

odoo.define("prt_mail_messages_pro/static/src/components/chatter_topbar/chatter_topbar.js", function (require) {
    "use strict";

    const components = {
        ChatterTopbar: require("mail/static/src/components/chatter_topbar/chatter_topbar.js"),
    };
    const { patch } = require("web.utils");

    patch(components.ChatterTopbar, "prt_mail_messages_pro/static/src/components/chatter_topbar/chatter_topbar.js", {
        _onClickShowNotifications(ev) {
            if (this.chatter.thread.displayNotifications) {
                this.chatter.thread.update({ displayNotifications: false });
            } else {
                this.chatter.thread.update({ displayNotifications: true });
            }
            return this.chatter.saveThreadFilters("displayNotifications", "hide_notifications")
        },
        _onClickShowNotes(ev) {
            if (this.chatter.thread.displayNotes) {
                this.chatter.thread.update({ displayNotes: false });
            } else {
                this.chatter.thread.update({ displayNotes: true });
            }
            return this.chatter.saveThreadFilters("displayNotes", "hide_notes")
        },
        _onClickShowMessages(ev) {
            if (this.chatter.thread.displayMessages) {
                this.chatter.thread.update({ displayMessages: false });
            } else {
                this.chatter.thread.update({ displayMessages: true });
            }
            return this.chatter.saveThreadFilters("displayMessages", "hide_messages");
        },
    });

});
