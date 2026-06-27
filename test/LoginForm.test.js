import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import LoginForm from '../LoginForm';

jest.mock('../api', () => ({
  login: jest.fn(() => Promise.resolve({ success: true }))
}));

describe('LoginForm', () => {
  test('shows loading spinner on submit', async () => {
    render(<LoginForm />);

    const submitButton = screen.getByRole('button', { name: /submit/i });
    const spinner = screen.queryByTestId('loading-spinner');

    expect(spinner).not.toBeInTheDocument();

    fireEvent.click(submitButton);

    expect(screen.getByTestId('loading-spinner')).toBeVisible();
  });

  test('hides loading spinner after submit', async () => {
    render(<LoginForm />);

    const submitButton = screen.getByRole('button', { name: /submit/i });

    fireEvent.click(submitButton);

    // Wait for the spinner to disappear
    await screen.findByRole('button', { name: /submit/i });
    expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
  });
});
