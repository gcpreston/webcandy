import React from 'react';
import axios from 'axios';
import ChromePicker from 'react-color';
import {
    Button,
    Form,
    Col,
    Overlay,
    Popover,
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
    }

    // TODO: Better way to do this?
    componentWillMount() {
        axios.get("/scripts").then(response => {
            this.setState({ scripts: response.data.scripts });
        });

        axios.get("/colors").then(response => {
            let colors = response.data;
            this.setState({ colors: colors });

            // Set currentColor initial value
            if (colors) {
                this.setState({ currentColor: Object.values(colors)[0] })
            }
        });
    }

    // TODO: Make popover work when window width is smaller than expected
    render() {
        return (
            <Form onSubmit={this.handleSubmit}>
                <Form.Group controlId="script">
                    <Form.Label>Script</Form.Label>
                    <Form.Control as="select"
                                  disabled={this.state.solidColor}>
                        {this.state.scripts.map((name, idx) => {
                            return <option key={idx}>{name}</option>;
                        })}
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId="solidColorCheck">
                    <Form.Check value={this.state.solidColor}
                                onChange={this.handleSolidColorCheck}
                                label="Solid color"/>
                </Form.Group>

                {this.state.solidColor ?
                    <React.Fragment>

                        <Form.Label>Color entry</Form.Label>
                        <Form.Row>
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
                            <Form.Group as={Col} controlId="colorField">
                                <Overlay target={this.refs.colorField}
                                         show={this.state.customColor}
                                         placement="right">
                                    <Popover>
                                        <ChromePicker
                                            color={this.state.currentColor}
                                            onChange={e => this.updateCurrentColor(e.hex)}/>
                                    </Popover>
                                </Overlay>
                                <Form.Control ref="colorField"
                                              type="text"
                                              placeholder="#RRGGBB"
                                              value={this.state.currentColor}
                                              onChange={e => this.updateCurrentColor(e.target.value)}
                                              disabled={!this.state.customColor}/>
                            </Form.Group>
                        </Form.Row>

                        <Form.Group controlId="customColorCheck">
                            <Form.Check value={this.state.customColor}
                                        onChange={this.handleCustomColorCheck}
                                        label="Custom color"/>
                        </Form.Group>
                    </React.Fragment> : null}

                <Form.Group controlId="submitButton">
                    <Button variant="primary" type="submit">
                        Submit
                    </Button>
                </Form.Group>

                <Form.Group controlId="offButton">
                    <Button variant="danger" onClick={this.handleOff}>
                        Turn off
                    </Button>
                </Form.Group>
            </Form>
        );
    }

    /**
     * Update the currently entered color.
     * @param color - The new color
     */
    updateCurrentColor = (color) => {
        this.setState({ currentColor: color });
    };

    /**
     * Change whether the user can select a script or a solid color.
     * @param event - The change event from the checkbox
     */
    handleSolidColorCheck = (event) => {
        this.setState({ solidColor: event.target.checked })
    };

    /**
     * Update the currently entered color based on a select change event.
     * @param event - The change event from the select
     */
    handleColorSelect = (event) => {
        this.setState({ currentColor: this.state.colors[event.target.value] });
    };

    /**
     * Change whether the user can type the hex of a custom color or select from
     * the list of saved colors.
     * @param event - The change event from the checkbox
     */
    handleCustomColorCheck = (event) => {
        this.setState({ customColor: event.target.checked })
    };

    /**
     * Submit the form data.
     * @param event - The submit event
     */
    handleSubmit = (event) => {
        event.preventDefault();

        const target = event.currentTarget;

        let script, color;

        if (this.state.solidColor) {
            script = "solid_color"
        } else {
            script = target["script"].value;
        }

        if (this.state.customColor) {
            color = target["colorField"].value;
        } else if (target["colorSelect"]) {
            color = this.state.colors[target["colorSelect"].value]
        }

        const form = new FormData();
        form.set("script", script);
        form.set("color", color);

        axios.post("/submit", form)
            .then(response => console.log(response))
            .catch(error => console.log(error));
    };

    /**
     * Submit a request to turn off the lights.
     * @param event - The "Turn off" button event
     */
    handleOff = (event) => {
        event.preventDefault();

        const form = new FormData();
        form.set("script", "off");

        axios.post("/submit", form)
            .then(response => console.log(response))
            .catch(error => console.log(error));
    }
}
