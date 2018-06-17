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
            this.callbacks[++id] = cb;
            msg['cb_id'] = id;
        }
    }

    _call_cb(id, data) {
        if (id) {
            this.callbacks[id](data);
            delete this.callbacks[id];
        }
    }

    login(login, password, cb) {
        let msg = {method: "login", login: login, password: password};
        this._cb_check(msg, cb);
        this.socket.send(JSON.stringify(msg));
    }

};
