const ws = new WebSocket("ws://localhost:42069")

ws.onerror = (err) => {
    console.error("It's joever", err);
}

