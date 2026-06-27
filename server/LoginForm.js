import React from 'react';
import { Spinner } from './Spinner';

function LoginForm() {
  return (
    <form>
      <h2>Login</h2>
      <label>
        Username:
        <input type="text" name="username" />
      </label>
      <label>
        Password:
        <input type="password" name="password" />
      </label>
      <button type="submit">Submit</button>
    </form>
  );
}

export default LoginForm;