enum ConnectionState {
    CONNECTING = 0,
    CONNECTED = 1,
    ERROR = 2,
    CLOSE = 3,
}

export class WS {
    private ws: WebSocket | undefined;
    private url: string;
    private state: ConnectionState | undefined;

    constructor(url: string) {
        this.url = url;
        this.connect();
    }

    private connect(): void {
        const ws = this.ws = new WebSocket(this.url);
        this.state = ConnectionState.CONNECTING

        ws.onopen = () => {
            this.state = ConnectionState.CONNECTED
        }

        ws.onerror = async () => {
            this.state = ConnectionState.ERROR
            await new Promise(resolve => setTimeout(resolve, 1000));
            this.connect();
        }
    }

    public send(data: string) {
        if (this.state === ConnectionState.CONNECTED) {
            this.ws?.send(data);
        }
    }
}
