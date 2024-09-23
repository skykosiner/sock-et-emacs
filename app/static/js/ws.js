var ConnectionState;
(function (ConnectionState) {
    ConnectionState[ConnectionState["CONNECTING"] = 0] = "CONNECTING";
    ConnectionState[ConnectionState["CONNECTED"] = 1] = "CONNECTED";
    ConnectionState[ConnectionState["ERROR"] = 2] = "ERROR";
    ConnectionState[ConnectionState["CLOSE"] = 3] = "CLOSE";
})(ConnectionState || (ConnectionState = {}));
export class WS {
    ws;
    url;
    state;
    constructor(url) {
        this.url = url;
        this.connect();
    }
    connect() {
        const ws = this.ws = new WebSocket(this.url);
        this.state = ConnectionState.CONNECTING;
        ws.onopen = () => {
            this.state = ConnectionState.CONNECTED;
        };
        ws.onerror = async () => {
            this.state = ConnectionState.ERROR;
            await new Promise(resolve => setTimeout(resolve, 1000));
            this.connect();
        };
    }
    send(data) {
        if (this.state === ConnectionState.CONNECTED) {
            this.ws?.send(data);
        }
    }
}
