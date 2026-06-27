import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import UserInfoForm from './UserInfoForm';

describe('UserInfoForm', () => {
  test('renders the form with all fields', () => {
    render(<UserInfoForm />);
    expect(screen.getByLabelText(/first name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/last name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });

  test('submits the form with entered input', () => {
    const handleSubmit = jest.fn();
    render(<UserInfoForm onSubmit={handleSubmit} />);

    fireEvent.change(screen.getByLabelText(/first name/i), {
      target: { value: 'John' },
    });
    fireEvent.change(screen.getByLabelText(/last name/i), {
      target: { value: 'Doe' },
    });
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'john.doe@example.com' },
    });

    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(handleSubmit).toHaveBeenCalledWith({
      firstName: 'John',
      lastName: 'Doe',
      email: 'john.doe@example.com',
    });
  });

  test('displays validation error messages when fields are empty', () => {
    render(<UserInfoForm />);

    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(screen.getByText(/first name is required/i)).toBeVisible();
    expect(screen.getByText(/last name is required/i)).toBeVisible();
    expect(screen.getByText(/email is required/i)).toBeVisible();
  });

  test('shows email validation error when email is invalid', () => {
    render(<UserInfoForm />);

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'invalid-email' },
    });

    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(screen.getByText(/email is not valid/i)).toBeVisible();
  });
});