import React from 'react';
import { Form, Button } from 'react-bootstrap';
import Cookies from 'js-cookie';
import axios from 'axios';

import LightConfigForm from '../forms/LightConfigForm';
import logo from "../../img/webcandy_logo.png";
import { getAuthConfig } from "../util";

/**
 * Webcandy main app page.
 */
export default class App extends React.Component {
    state = {
        username: "",
        connectedClients: [],
        clientId: ""
    };

    componentWillMount() {
        // TODO: Figure out better way to handle errors for production
        this.updateConnectedClients();

        axios.get("/api/user/info", getAuthConfig()).then(response => {
            const data = response.data;
            this.setState({ username: data['username'] })
        }).catch(error => {
            // TODO: Redirect to login directly from index.jsx
            if (error.response && error.response.status === 401) {
                window.location = "/login"; // api key has expired
            } else {
                console.log(error);
            }
        });
    }

    render() {
        return (
            <React.Fragment>
                <img className="centerImage" src={logo} alt="Webcandy logo"/>
                <div className="title">
                    <p>Logged in as {this.state.username}</p>
                    <p>Cookie: {Cookies.get("token")}</p>
                </div>

                <div className="clientSelect">
                    <Form>
                        <Form.Group controlId="clientSelect">
                            {this.state.connectedClients.length === 0 ?
                                <Form.Text>No clients currently
                                    connected.</Form.Text> :
                                <React.Fragment>
                                    <Form.Label>Client</Form.Label>
                                    <Form.Control as="select"
                                                  onChange={e => this.setState({ clientId: e.target.value })}>
                                        {this.state.connectedClients.map((name, idx) => {
                                            return <option
                                                key={idx}>{name}</option>;
                                        })}
                                    </Form.Control>
                                </React.Fragment>}
                        </Form.Group>

                        <Form.Group controlId="refreshButton">
                            <Button onClick={this.updateConnectedClients}>
                                Refresh
                            </Button>
                        </Form.Group>
                    </Form>
                </div>

                <hr/>

                {this.state.clientId ?
                    <LightConfigForm clientId={this.state.clientId}/> :
                    null}

                <Button variant="warning" onClick={this.handleLogout}>
                    Logout
                </Button>
            </React.Fragment>
        )
    }

    updateConnectedClients = () => {
        axios.get("/api/user/clients", getAuthConfig()).then(response => {
            const connectedClients = response.data;
            this.setState({ connectedClients: connectedClients });

            if (connectedClients.length > 0) {
                // set initial clientId value if not already set
                if (!this.state.clientId) {
                    this.setState({ clientId: connectedClients[0] });
                }
            } else {
                // clear clientId if no clients are connected
                this.setState({ clientId: "" });
            }
        }).catch(error => console.log(error));
    };

    handleLogout = () => {
        Cookies.remove("token");
        window.location = "/login";
    };
}
