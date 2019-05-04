import React from 'react';
import LoginForm from './forms/LoginForm';

export default class Login extends React.Component {
    render() {
        return (
            <React.Fragment>
                <div className="title">
                    <h1 className="center">Log in</h1>
                </div>
                <LoginForm/>
            </React.Fragment>
        )
    }
}
