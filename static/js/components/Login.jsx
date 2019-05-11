import React from 'react';
import { Button } from "react-bootstrap";

import LoginForm from './forms/LoginForm';

/**
 * Login page.
 */
export default class Login extends React.Component {
    render() {
        return (
            <React.Fragment>
                <div className="title">
                    <h1 className="center">Log in</h1>
                </div>
                <LoginForm/>
                <Button variant="warning" onClick={() => window.location = '/create-account'}>
                    Create Account
                </Button>
            </React.Fragment>
        )
    }
}
