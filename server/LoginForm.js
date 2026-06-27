import React, { useState } from 'react';
import Spinner from './Spinner';

const LoginForm = () => {
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        // Simulate the loading delay
        await new Promise(resolve => setTimeout(resolve, 2000));
        setLoading(false);
        // Handle the form submission logic here
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" placeholder="Username" />
            <input type="password" placeholder="Password" />
            <button type="submit">
                {loading ? <Spinner /> : 'Submit'}
            </button>
        </form>
    );
};

export default LoginForm;