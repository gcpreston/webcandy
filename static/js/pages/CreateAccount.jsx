import React from 'react';
import { Button } from 'react-bootstrap';

import CreateAccountForm from './forms/CreateAccountForm';

/**
 * Account creation page.
 */
export default class CreateAccount extends React.Component {
    render() {
        return (
            <React.Fragment>
                <div className="title">
                    <h1 className="center">Create account</h1>
                </div>
                <CreateAccountForm/>
                <Button variant="warning" onClick={() => window.location = '/login'}>
                    Login
                </Button>
            </React.Fragment>
        )
    }
}
