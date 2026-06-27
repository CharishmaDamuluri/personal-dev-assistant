import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import LoginForm from '../LoginForm';


describe('LoginForm', () => {
    test('spinner is visible during form submission', async () => {
        render(<LoginForm />);
        
        const submitButton = screen.getByText('Submit');
        const usernameInput = screen.getByLabelText('Username');
        const passwordInput = screen.getByLabelText('Password');

        fireEvent.change(usernameInput, { target: { value: 'testuser' } });
        fireEvent.change(passwordInput, { target: { value: 'password' } });
        
        fireEvent.click(submitButton);

        const spinner = await screen.findByTestId('loading-spinner');
        expect(spinner).toBeVisible();
    });

    // other tests
});