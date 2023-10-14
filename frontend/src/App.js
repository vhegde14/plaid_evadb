import './App.css';

import React, { useState, useEffect } from 'react';

import { usePlaidLink } from 'react-plaid-link';

function App() {
    const [linkToken, setLinkToken] = useState('token');
    const [publicToken, setPublicToken] = useState(false);

    useEffect(() => {
        createLinkToken();
    }, [])

    const { open, ready } = usePlaidLink({
        token: linkToken,
        onSuccess: (public_token, metadata) => {
            // send public_token to server
            console.log('Public Token: ' + public_token);
            setPublicToken(true);
            const response = fetch('http://127.0.0.1:8000/set_access_token', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({ public_token: public_token}),
            });
            console.log(response);
        },
    });

    const createLinkToken = async () => {
        await fetch('http://127.0.0.1:8000/create_link_token', {
            method: "POST"
        })
        .then(response => response.json())
        .then(data => {
            setLinkToken(data['link_token']);
            console.log('Link Token: ' + data['link_token']);
        })
        .catch(error => console.error(error));
    };

    return (
        <div className="app">
            <p className="header">Plaid with EvaDB</p>
            <div className="main">
                <div className="buttons">
                    <button className="plaid-button" onClick={() => open()} disabled={!ready}>
                        Connect a bank account
                    </button>
                </div>
                {linkToken === 'token' ? <p>Link Token not provided</p> : <p>Plaid link token authenticated</p>}
                {publicToken ? <p>Link Token exchanged for Public Token</p> : <p>Public Token not exchanged</p>}
            </div>
        </div>
    );
}

export default App;
