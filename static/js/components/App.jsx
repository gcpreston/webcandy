import React from 'react';
import { Button } from 'react-bootstrap';
import LightConfigForm from './forms/LightConfigForm';

export default class App extends React.Component {

    render() {
        return (
            <React.Fragment>
                <h1 className="title">Webcandy</h1>
                <LightConfigForm/>
                <Button variant="warning" onClick={this.handleLogout}>
                    Logout
                </Button>
            </React.Fragment>
        )
    }

    handleLogout = () => {
        sessionStorage.removeItem("token");
        window.location = "/login";
    }
}
