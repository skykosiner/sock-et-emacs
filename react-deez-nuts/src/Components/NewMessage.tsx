import { useState } from "react";
import { ReadyState } from "react-use-websocket";
import { useWebSocket } from "react-use-websocket/dist/lib/use-websocket";

export default function NewMessage(): JSX.Element {
    const [newMessage, setNewMessage] = useState<string>("");
    // const { sendMessage, readyState } = useWebSocket("wss://skykosiner.com:8080");
    const { sendMessage, readyState } = useWebSocket("ws://10.0.0.73:42069");

    function sendMessageForm(e: React.FormEvent) {
        e.preventDefault();

        if (readyState === ReadyState.OPEN) {
            sendMessage(newMessage);
        }
    }

    return (
        <form onSubmit={sendMessageForm} className="messageForm" style={{ paddingBottom: "5rem" }}>
            <input type="text" value={newMessage} onChange={(e) => setNewMessage(e.target.value)} placeholder="Message: " />
            <input type="submit" value="Send Message" style={{ cursor: "pointer" }} />
        </form>
    );
}
