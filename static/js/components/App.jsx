import React from 'react';
import { Button } from 'react-bootstrap';
import axios from 'axios';
import LightConfigForm from './forms/LightConfigForm';

/**
 * Webcandy main app page.
 */
export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            username: "",
            clientConnected: false
        };
    }

    componentWillMount() {
        // TODO: Figure out better way to handle errors for production
        this.updateClientConnected();

        axios.get("/api/user_info", {
            headers: {
                "Authorization": "Bearer " + sessionStorage.getItem("token")
            }
        }).then(response => {
            const data = response.data;
            this.setState({ username: data['username'] })
        }).catch(error => console.log(error.response));
    }

    render() {
        return (
            <React.Fragment>
                <div className="title">
                    <h1>Webcandy</h1>
                    <p>Logged in as {this.state.username}</p>
                </div>
                {this.state.clientConnected ? <LightConfigForm/> :
                    <React.Fragment>
                        <span>No clients currently connected. </span>
                        <Button onClick={this.updateClientConnected}>
                            Refresh
                        </Button>
                        <br/>
                    </React.Fragment>}
                <Button variant="warning" onClick={this.handleLogout}>
                    Logout
                </Button>
            </React.Fragment>
        )
    }

    updateClientConnected = () => {
        axios.get("/api/clients", {
            headers: {
                "Authorization": "Bearer " + sessionStorage.getItem("token")
            }
        }).then(response => {
            const clientConnected = response.data;
            this.setState({ clientConnected: clientConnected })
        }).catch(error => console.log(error.response));
    };

    handleLogout = () => {
        sessionStorage.removeItem("token");
        window.location = "/login";
    };
}
