import React from 'react';
import { useState } from 'react';
import { Spinner } from 'components/common/Spinner';

function LoginForm() {
  const [loading, setLoading] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    setLoading(true);
    // simulate login operation
    setTimeout(() => {
      setLoading(false);
    }, 2000);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" name="username" placeholder="Username" required />
      <input type="password" name="password" placeholder="Password" required />
      <button type="submit" disabled={loading}>Login</button>
      {loading && <Spinner />}
    </form>
  );
}

export default LoginForm;