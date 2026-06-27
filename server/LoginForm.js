import React, { useState } from 'react';

function LoginForm() {
    const [loading, setLoading] = useState(false);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    function handleFormSubmission(event) {
        event.preventDefault();
        setLoading(true);
        // Simulate form submission
        setTimeout(() => {
            setLoading(false);
            console.log('Form submitted:', { username, password });
        }, 2000);
    }

    return (
        <form onSubmit={handleFormSubmission}>
            <div>
                <label>Username:</label>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
            </div>
            <div>
                <label>Password:</label>
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </div>
            <button type="submit" disabled={loading}>
                {loading ? 'Loading...' : 'Submit'}
            </button>
        </form>
    );
}

export default LoginForm;