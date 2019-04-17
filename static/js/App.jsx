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
            patterns: [],
            currentPattern: "",
            colors: {},
            customColor: false,
            currentColor: "",
            colorLists: {},
            currentColorList: "",
            strobe: false,
        };
    }

    /**
     * Get values from Webcandy API and set state before app renders.
     */
    componentWillMount() {
        axios.get("/patterns").then(response => {
            const patterns = response.data;
            this.setState({ patterns: patterns });

            // set currentPattern initial value
            if (patterns) {
                this.setState({ currentPattern: Object.values(patterns)[0] })
            }
        });

        axios.get("/colors").then(response => {
            const colors = response.data;
            this.setState({ colors: colors });

            // set currentColor initial value
            if (colors) {
                this.setState({ currentColor: Object.values(colors)[0] })
            }
        });

        axios.get("/color_lists").then(response => {
            const colorLists = response.data;
            this.setState({ colorLists: colorLists });

            // set currentColorList initial value
            if (colorLists) {
                this.setState({ currentColorList: Object.values(colorLists)[0] })
            }
        })
    }

    // TODO: Make popover work when window width is smaller than expected
    render() {
        // TODO: Speed entry

        const colorEntry = (
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
                                    onChange={e => this.setState({ currentColor: e.hex })}/>
                            </Popover>
                        </Overlay>
                        <Form.Control ref="colorField"
                                      type="text"
                                      placeholder="#RRGGBB"
                                      value={this.state.currentColor}
                                      onChange={e => this.setState({ currentColor: e.target.value })}
                                      disabled={!this.state.customColor}/>
                    </Form.Group>
                </Form.Row>

                <Form.Group controlId="customColorCheck">
                    <Form.Check value={this.state.customColor}
                                onChange={this.handleCustomColorCheck}
                                label="Custom color"/>
                </Form.Group>
            </React.Fragment>
        );

        let colorListEntry = (
            <Form.Row>
                <Form.Group as={Col} controlId="colorListSelect">
                    <Form.Label>Color list entry</Form.Label>
                    <Form.Control as="select"
                                  onChange={this.handleColorListSelect}>
                        {Object.keys(this.state.colorLists).map((name, idx) => {
                            return <option
                                key={idx}>{name}</option>;
                        })}
                    </Form.Control>
                </Form.Group>
            </Form.Row>
        );

        let config;
        switch (this.state.currentPattern) {
            case "fade":
            case "scroll":
                config = colorListEntry;
                break;
            case "solid_color":
                config = colorEntry;
                break;
        }

        return (
            <Form onSubmit={this.handleSubmit}>
                <Form.Group controlId="config">
                    <Form.Label>Pattern</Form.Label>
                    <Form.Control as="select"
                                  onChange={e => this.setState({ currentPattern: e.target.value })}>
                        {this.state.patterns.map((name, idx) => {
                            return <option key={idx}>{name}</option>;
                        })}
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId="strobeCheck">
                    <Form.Check value={this.state.strobe}
                                onChange={e => this.setState({ strobe: e.target.checked })}
                                label="Strobe"/>
                </Form.Group>

                {config}

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
     * Update the currently entered color based on a select change event.
     * @param event - The change event from the select
     */
    handleColorSelect = (event) => {
        this.setState({ currentColor: this.state.colors[event.target.value] });
    };

    /**
     * Update the currently entered color list based on a select change event.
     * @param event - The change event from the select
     */
    handleColorListSelect = (event) => {
        this.setState({ currentColorList: this.state.colorLists[event.target.value] })
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

        let pattern = target["config"].value;
        let config = {};

        // set strobe field (must convert string to bool server-side)
        config["strobe"] = this.state.strobe ? "True" : "False";

        // set color field
        if (this.state.customColor) {
            config["color"] = target["colorField"].value;
            config["color"] = target["colorField"].value;
        } else if (target["colorSelect"]) {
            config["color"] = this.state.colors[target["colorSelect"].value];
        }

        // set color_list field
        if (target["colorListSelect"]) {
            config["color_list"] = this.state.colorLists[target["colorListSelect"].value];
        }

        const form = new FormData();
        form.set("pattern", pattern);
        form.set("config", JSON.stringify(config));

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
        form.set("pattern", "off");
        form.set("config", JSON.stringify({}));  // emtpy config

        axios.post("/submit", form)
            .then(response => console.log(response))
            .catch(error => console.log(error));
    }
}
