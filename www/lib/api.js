import { get } from "./storage.js"

export default class API {

    constructor(address) {
        this.socket = new WebSocket(address);

        this.id = 0;
        this.callbacks = {};
    }

    onopen(handler)   { this.socket.onopen    = handler;    }
    onclose(handler)  { this.socket.onclose   = handler;   }
    onerror(handler)  { this.socket.onerror   = handler;   }
    onmessage(handler){ this.socket.onmessage = handler; }

    // TODO: Add more methods

    _cb_check(msg, cb) {
        if (cb) {
            this.callbacks[++this.id] = cb;
            msg['cb_id'] = this.id;
        }
    }

    _call_cb(id, data) {
        if (id !== 0) {
            this.callbacks[id](data);
            delete this.callbacks[id];
        }
    }

    login(login, password, cb) {
        let msg = {method: "login", login: login, password: password};
        this._cb_check(msg, cb);
        this.socket.send(JSON.stringify(msg));
    }

    check_auth(cb) {
        let msg = {method: "check_auth", session: get("session")};
        this._cb_check(msg, cb);
        this.socket.send(JSON.stringify(msg));
    }

};
