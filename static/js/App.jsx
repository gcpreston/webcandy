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
            customColor: false,
            currentColor: "",
        };

        this.handleScriptSelect = this.handleScriptSelect.bind(this);
        this.handleColorSelect = this.handleColorSelect.bind(this);
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
                    <Form.Control as="select" onChange={this.handleScriptSelect}>
                        {this.state.scripts.map((name, idx) => {
                            return <option key={idx}>{name}</option>;
                        })}
                    </Form.Control>
                </Form.Group>

                {this.state.solidColor ?
                    <React.Fragment>
                        <Form.Label>Color entry</Form.Label>
                        <Form.Row>
                            <Form.Group as={Col} controlId="colorField">
                                <Form.Control type="text"
                                              placeholder="#RRGGBB"
                                              value={this.state.currentColor}
                                              onChange={this.handleColorInput}
                                              disabled={!this.state.customColor}/>
                            </Form.Group>
                            <Form.Group as={Col} controlId="colorSelect">
                                <Form.Control as="select"
                                              disabled={this.state.customColor}
                                              onChange={this.handleColorSelect}>
                                    {Object.keys(this.state.colors).map((name, idx) => {
                                        return <option
                                            key={idx}>{name}</option>;
                                    })}
                                </Form.Control>
                            </Form.Group>
                        </Form.Row>
                        <Form.Group controlId="customColorCheck">
                            <Form.Check value={this.state.customColor}
                                        onChange={this.handleCustomColorCheck}
                                        label="Custom color"/>
                        </Form.Group>
                    </React.Fragment> : null}

                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
        );
    }

    /**
     * Update state to indicate if the solid_color script is selected.
     * @param event - The script selection event
     */
    handleScriptSelect(event) {
        if (event.target.value === "solid_color") {
            this.setState({solidColor: true});
        } else {
            this.setState({solidColor: false});
        }
    }

    /**
     * Update the currently entered color based on an input change event.
     * @param event - The change event from the text input
     */
    handleColorInput(event) {
        this.setState({currentColor: event.target.value})
    }

    /**
     * Update the currently entered color based on a select change event.
     * @param event - The change event from the select
     */
    handleColorSelect(event) {
        this.setState({currentColor: this.state.colors[event.target.value]});
    }

    /**
     * Change whether the user can type the hex of a custom color or select from
     * the list of saved colors.
     * @param event - The change event from the checkbox
     */
    handleCustomColorCheck(event) {
        this.setState({customColor: event.target.checked})
    }

    handleSubmit(event) {
        event.preventDefault();

        const target = event.currentTarget;

        let form = new FormData();
        form.set("script", target["script"].value);
        form.set("color", target["colorField"] ? target["colorField"].value : null);

        axios.post("/submit", form)
            .then(response => console.log(response))
            .catch(error => console.log(error));
    }
}
