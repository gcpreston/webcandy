import React from 'react';
import axios from 'axios';
import {
    Button,
    Form,
    Col
} from 'react-bootstrap';

export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            scripts: [],
            colors: {},
            solidColor: false,
            colorEntryDisabled: true,
            currentColor: "",
        };

        this.updateSolidColor = this.updateSolidColor.bind(this);
        this.updateCurrentColor = this.updateCurrentColor.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    // TODO: Better way to do this?
    componentWillMount() {
        axios.get("/scripts").then(response => {
            this.setState({scripts: response.data.scripts});
        });

        axios.get("/colors").then(response => {
            let colors = response.data.colors;
            this.setState({colors: colors});

            // Set currentColor initial value
            if (colors) {
                this.setState({currentColor: Object.values(colors)[0]})
            }
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
                    <React.Fragment>
                        <Form.Label>Color entry</Form.Label>
                        <Form.Row>
                            <Form.Group as={Col} controlId="color">
                                <Form.Control type="text"
                                              placeholder="#RRGGBB"
                                              value={this.state.currentColor}
                                              disabled={this.state.colorEntryDisabled}/>
                            </Form.Group>
                            <Form.Group as={Col}>
                                <Form.Control as="select"
                                              onChange={this.updateCurrentColor}>
                                    {Object.keys(this.state.colors).map((name, idx) => {
                                        return <option
                                            key={idx}>{name}</option>;
                                    })}
                                </Form.Control>
                            </Form.Group>
                        </Form.Row>
                    </React.Fragment> : null}

                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
        );
    }

    /**
     * Update state to indicate if solid_color is selected.
     *
     * @param event - The script selection event
     */
    updateSolidColor(event) {
        if (event.target.value === "solid_color") {
            this.setState({solidColor: true});
        } else {
            this.setState({solidColor: false});
        }
    }

    /**
     * Update state to reflect currently selected saved color.
     *
     * @param event - The color selection event
     */
    updateCurrentColor(event) {
        this.setState({currentColor: this.state.colors[event.target.value]});
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
            .catch(error => console.log(error));
    }
}
