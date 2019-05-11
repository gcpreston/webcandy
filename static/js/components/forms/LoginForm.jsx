import React from 'react';
import axios from 'axios';
import { Button, Form } from 'react-bootstrap';

/**
 * Login form.
 */
export default class LoginForm extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            username: "",
            password: "",
            errors: [],
        };
    }

    // TODO: Remember me
    render() {
        return (
            <React.Fragment>
                {this.state.errors ?
                    <ul className="errors">
                        {this.state.errors.map((msg, idx) => <li key={idx}>{msg}</li>)}
                    </ul> : null}

                <Form onSubmit={this.handleSubmit}>
                    <Form.Group controlId="username">
                        <Form.Label>Username</Form.Label>
                        <Form.Control type="text"
                                      value={this.state.username}
                                      onChange={e => this.setState({ username: e.target.value })}/>
                    </Form.Group>

                    <Form.Group controlId="password">
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password"
                                      value={this.state.password}
                                      onChange={e => this.setState({ password: e.target.value })}/>
                    </Form.Group>

                    <Form.Group controlId="submitButton">
                        <Button variant="primary" type="submit">
                            Submit
                        </Button>
                    </Form.Group>
                </Form>
            </React.Fragment>
        );
    }

    handleSubmit = (event) => {
        event.preventDefault();

        const data = {
            "username": this.state.username,
            "password": this.state.password
        };

        axios.post("/api/token", data).then(response => {
            const token = response.data["token"];
            sessionStorage.setItem("token", token);
            window.location = "/";
        }).catch(error => {
            if (error.response.status === 401) {
                this.setState({ errors: [error.response.data["error_description"]] })
            } else {
                console.log(error);
            }
        });
    }
}
