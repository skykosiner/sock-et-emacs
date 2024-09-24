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
                    <button>Flicker Ligths</button>
                    <button>Turn Me On 😳</button>
                    <button>That's What She Said</button>
                    <button onClick={() => setShowHelp(!showHelp)}>Message Commands - Help {showHelp && <p>Hide</p>}</button>
                </div>

                {showHelp && (
                    <div>
                        <h3>Vim Normal Mode Commands</h3>
                        <ul>
                            {vimCommands.map(cmd => (
                                <li>{cmd}</li>
                            ))}
                        </ul>

                        <h3 style={{ paddingTop: "0.5rem" }}>Inserting Into Vim Commands</h3>
                        <p>Insert into vim with <code>!vi</code>. Followed by the text you want to insert</p>
                        <p>Insert after into vim with <code>!va</code>. Followed by the text you want to insert</p>
                    </div>
                )}

                <NewMessage />
            </div>
        </div>
    );
}
