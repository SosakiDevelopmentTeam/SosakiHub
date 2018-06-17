export default class API {

    constructor(address) {
        this.socket = new WebSocket(address);
    }

    onopen(handler)   { this.socket.onopen(handler);    }
    onclose(handler)  { this.socket.onclose(handler);   }
    onerror(handler)  { this.socket.onerror(handler);   }
    onmessage(handler){ this.socket.onmessage(handler); }

    // TODO: Add more methods
    
    login(login, password) {
        let msg = {method: "login", login: login, password: password};
        if (this.socket.CLOSED)
            throw "Socket is closed!";
        msg.send(JSON.stringify(msg));
    }

};
