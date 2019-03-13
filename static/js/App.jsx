import React from 'react';
import axios from 'axios';
import Dropdown from 'react-bootstrap/Dropdown';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Col from "react-bootstrap/Col";

export default class App extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            scripts: [],
        };

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    // TODO: Better way to do this?
    componentWillMount() {
        axios.get("/scripts").then(response => {
            this.setState({scripts: response.data.scripts});
        });
    }

    renderDropdown() {
        return (
            <Dropdown id="configs">
                <Dropdown.Toggle>
                    Configurations
                </Dropdown.Toggle>
                <Dropdown.Menu>
                    {this.state.scripts.map((name, idx) => {
                        return (
                            <Dropdown.Item key={idx}
                                           onClick={this.handleClick(name)}>
                                {name}
                            </Dropdown.Item>
                        );
                    })}
                </Dropdown.Menu>
            </Dropdown>
        );
    }

    render() {
        return (
            <Form onSubmit={this.handleSubmit}>
                <Form.Row>
                    <Form.Group as={Col} controlId="script">
                        <Form.Label>Script</Form.Label>
                        <Form.Control as="select">
                            {this.state.scripts.map((name, idx) => {
                                return <option key={idx}>{name}</option>;
                            })}
                        </Form.Control>
                    </Form.Group>
                </Form.Row>

                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
        );
    }

    handleClick(script) {
        return () => axios.get(`/run/${script}`)
            .then(response => console.log(response))
            .catch(error => console.log(error));
    }

    handleSubmit(event) {
        event.preventDefault();

        const target = event.currentTarget;

        let form = new FormData();
        form.set("script", target["script"].value);
        form.set("color", null);  // TODO: Set color

        axios.post("/submit", form)
            .then(response => console.log(response))
            .catch(error => console.log(error));
    }
}
