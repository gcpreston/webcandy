import React from 'react';
import { Button, Form } from 'react-bootstrap';

/**
 * Account creation form.
 */
export default class CreateAccountForm extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            username: "",
            email: "",
            password: "",
            confirmPassword: "",
            errors: [],  // TODO: Implement account creation form validation
        };
    }

    render() {
        return (
            <React.Fragment>
                {this.state.errors ?
                    <ul className="errors">
                        {this.state.errors.map((msg, idx) => {
                            return <li key={idx}>{msg}</li>
                        })}
                    </ul> : null}

                <Form onSubmit={this.handleSubmit}>
                    <Form.Group controlId="username">
                        <Form.Label>Username</Form.Label>
                        <Form.Control type="text"
                                      value={this.state.username}
                                      onChange={e => this.setState({ username: e.target.value })}/>
                    </Form.Group>

                    <Form.Group controlId="email">
                        <Form.Label>Email</Form.Label>
                        <Form.Control type="email"
                                      value={this.state.email}
                                      onChange={e => this.setState({ email: e.target.value })}/>
                    </Form.Group>

                    <Form.Group controlId="password">
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password"
                                      value={this.state.password}
                                      onChange={e => this.setState({ password: e.target.value })}/>
                    </Form.Group>

                    <Form.Group controlId="confirmPassword">
                        <Form.Label>Confirm password</Form.Label>
                        <Form.Control type="password"
                                      value={this.state.confirmPassword}
                                      onChange={e => this.setState({ confirmPassword: e.target.value })}/>
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
        console.log(this.state);
    }
}
