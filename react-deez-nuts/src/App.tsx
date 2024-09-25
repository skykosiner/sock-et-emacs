import { useState } from "react";
import NewMessage from "./Components/NewMessage";

export default function App(): JSX.Element {
    const [showHelp, setShowHelp] = useState<boolean>(false);

    const vimCommands = [
        "dd", "gg", "G", "h", "j", "k", "l", "o", "O",
        "zz", ">>", "<<", "_", "v", "V", "A", "I", "J", "u",
    ]

    return (
        <div className="center">
            <div style={{ width: "30rem" }}>
                <h1 style={{ textAlign: "center" }}>Control Me Daddy</h1>

                <div className="buttons">
                    <a>Flicker Ligths</a>
                    <a>Turn Me On 😳</a>
                    <a>That's What She Said</a>
                    <button onClick={() => setShowHelp(!showHelp)}>Message Commands - Help {showHelp && <p>Hide</p>}</button>
                </div>

                {showHelp && (
                    <div>
                        <h2>Vim Commands</h2>
                        <h3 style={{ paddingTop: "0.5rem" }}>Vim Normal Mode Commands</h3>
                        <ul>
                            {vimCommands.map(cmd => (
                                <li>{cmd}</li>
                            ))}
                        </ul>

                        <h3 style={{ paddingTop: "0.5rem" }}>Inserting Into Vim Commands</h3>
                        <p>Insert into vim with <code>!vi</code>. Followed by the text you want to insert</p>
                        <p>Insert after into vim with <code>!va</code>. Followed by the text you want to insert</p>

                        <h2 style={{ paddingBottom: "0.5rem", paddingTop: "0.5rem" }}>System Commands</h2>
                        <ul>
                            <li><code>!turn off screen</code> turns off my main screen for 5 seconds</li>
                            <li><code>!change background</code> changes my background to a random one in my backgrounds folder</li>
                            <li><code>!i3 workspace</code> switches my i3 workspace to number 69 (nice)</li>
                            <li><code>asdf</code> changes my keyboard to utter chaos for 3 seconds so I can't type</li>
                        </ul>
                    </div>
                )}

                <NewMessage />
            </div>
        </div>
    );
}
