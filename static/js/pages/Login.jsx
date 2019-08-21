import React from 'react';
import { Button } from 'react-bootstrap';

import LoginForm from '../forms/LoginForm';
import logo from '../../img/webcandy_logo.png';

/**
 * Login page.
 */
export default class Login extends React.Component {
    render() {
        return (
            <React.Fragment>
                <img className="centerImage" src={logo} alt="Webcandy logo"/>
                <br/>
                <h3>Log in</h3>
                <LoginForm/>
                <Button variant="warning"
                        onClick={() => window.location = '/create-account'}>
                    Create Account
                </Button>
            </React.Fragment>
        )
    }
}
