import React from 'react';
import { Button } from 'react-bootstrap';
import axios from 'axios';
import LightConfigForm from './forms/LightConfigForm';

export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            username: ""
        };
    }

    componentWillMount() {
        axios.get("/api/get_user/me", {
            headers: {
                "Authorization": "Bearer " + sessionStorage.getItem("token")
            }
        }).then(response => {
            const data = response.data;
            this.setState({ username: data['username'] })
        });
    }

    render() {
        return (
            <React.Fragment>
                <h1 className="center">Webcandy</h1>
                <p className="center">Logged in as {this.state.username}</p>
                <div className="config">
                    <LightConfigForm/>
                    <Button variant="warning" onClick={this.handleLogout}>
                        Logout
                    </Button>
                </div>
            </React.Fragment>
        )
    }

    handleLogout = () => {
        sessionStorage.removeItem("token");
        window.location = "/login";
    }
}
