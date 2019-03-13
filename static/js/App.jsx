import React from 'react';
import axios from 'axios';
import {
    Button,
    Form,
} from 'react-bootstrap';

export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            scripts: [],
            solidColor: false,
        };

        this.updateSolidColor = this.updateSolidColor.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    // TODO: Better way to do this?
    componentWillMount() {
        axios.get("/scripts").then(response => {
            this.setState({scripts: response.data.scripts});
        });
    }

    render() {
        return (
            <Form onSubmit={this.handleSubmit}>
                <Form.Group controlId="script">
                    <Form.Label>Script</Form.Label>
                    <Form.Control as="select" onChange={this.updateSolidColor}>
                        {this.state.scripts.map((name, idx) => {
                            return <option key={idx}>{name}</option>;
                        })}
                    </Form.Control>
                </Form.Group>

                {this.state.solidColor ?
                <Form.Group controlId="color">
                    <Form.Label>Color entry</Form.Label>
                    <Form.Control type="text" size="sm" placeholder="#RRGGBB"/>
                </Form.Group> : null}

                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
        );
    }

    updateSolidColor(e) {
        if (e.target.value === "solid_color") {
            this.setState({ solidColor: true });
        } else {
            this.setState({ solidColor: false });
        }
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
        form.set("color", target["color"] ? target["color"].value : null);

        axios.post("/submit", form)
            .then(response => console.log(response))
            .catch(error => console.log(error));
    }
}
