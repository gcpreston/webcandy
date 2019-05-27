import React from 'react';
import { Form, Button } from 'react-bootstrap';
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
            connectedClients: [],
            clientId: ""
        };
    }

    componentWillMount() {
        // TODO: Figure out better way to handle errors for production
        this.updateConnectedClients();

        axios.get("/api/user/info", {
            headers: {
                "Authorization": "Bearer " + sessionStorage.getItem("token")
            }
        }).then(response => {
            const data = response.data;
            this.setState({ username: data['username'] })
        }).catch(error => console.log(error.response));
    }

    render() {
        const refreshButton = (
            <Button onClick={this.updateConnectedClients}>
                Refresh
            </Button>
        );

        return (
            <React.Fragment>
                <div className="title">
                    <h1>Webcandy</h1>
                    <p>Logged in as {this.state.username}</p>
                </div>

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
                        {refreshButton}
                    </Form.Group>
                </Form>

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
        axios.get("/api/user/clients", {
            headers: {
                "Authorization": "Bearer " + sessionStorage.getItem("token")
            }
        }).then(response => {
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
        }).catch(error => console.log(error.response));
    };

    handleLogout = () => {
        sessionStorage.removeItem("token");
        window.location = "/login";
    };
}
