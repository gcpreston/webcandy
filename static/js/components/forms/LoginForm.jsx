import React from 'react';
import axios from 'axios';
import { Button, Form } from 'react-bootstrap';

export default class LoginForm extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            username: "",
            password: "",
        };
    }

    // TODO: Remember me
    render() {
        return (
            <Form onSubmit={this.handleSubmit}>
                <Form.Group controlId="username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control type="text"
                                  value={this.state.username}
                                  onChange={e => this.setState({username: e.target.value})}/>
                </Form.Group>

                <Form.Group controlId="password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password"
                                  value={this.state.password}
                                  onChange={e => this.setState({password: e.target.value})}/>
                </Form.Group>

                <Form.Group controlId="submitButton">
                    <Button variant="primary" type="submit">
                        Submit
                    </Button>
                </Form.Group>
            </Form>
        );
    }

    handleSubmit = (event) => {
        event.preventDefault();

        const target = event.currentTarget;

        const data = {
            "username": target["username"].value,
            "password": target["password"].value
        };

        axios.post("/api/token", data).then(response => {
            const token = response.data["token"];
            sessionStorage.setItem("token", token);
            window.location = "/";
        }).catch(error => console.log(error));
    }
}
