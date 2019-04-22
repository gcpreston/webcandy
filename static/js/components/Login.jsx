import React from 'react';
import LoginForm from './forms/LoginForm';

export default class Login extends React.Component {
    render() {
        return (
            <React.Fragment>
                <h1 className="title">Log in</h1>
                <LoginForm/>
            </React.Fragment>
        )
    }
}
