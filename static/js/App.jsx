import React from 'react';
import axios from 'axios';
import { Button } from 'react-bootstrap';
import LightConfigForm from './components/LightConfigForm';

export default class App extends React.Component {
    render() {
        return (
            <React.Fragment>
                <h1 id="title">Webcandy</h1>
                <LightConfigForm/>
                <Button variant="warning" onClick={this.handleLogout}>
                    Logout
                </Button>
            </React.Fragment>
        )
    }

    handleLogout = () => {
        axios.post('/api/logout')
            .then(() => window.location = '/login')
            .catch(error => console.log(error))
    }
}
