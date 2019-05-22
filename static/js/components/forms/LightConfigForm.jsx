import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import ChromePicker from 'react-color';
import { Button, Col, Form, Overlay, Popover } from 'react-bootstrap';
import { getAuthConfig } from '../../util.js';

/**
 * Form for building lighting configuration request.
 */
export default class LightConfigForm extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            patterns: [],
            pattern: "",
            colors: {},
            color: "",
            selectedColor: "",  // name of color
            customColor: false,
            colorLists: {},
            colorList: [],
            selectedColorList: "",  // name of color list
            strobe: false,
        };
    }

    /**
     * Get the current color based on whether or not the "Custom oolor" checkbox
     * is selected.
     */
    getCurrentColor() {
        if (this.state.customColor) {
            return this.state.color
        } else {
            return this.state.colors[this.state.selectedColor];
        }
    }

    /**
     * Get values from Webcandy API and set state before app renders.
     */
    componentWillMount() {
        // make API calls
        const authConfig = getAuthConfig();
        const clientConfig = getAuthConfig();
        clientConfig["params"] = {"client_id": this.props.clientId};

        axios.get("/api/user/clients", clientConfig).then(response => {
            const patterns = response.data.patterns;
            this.setState({ patterns: patterns });

            // set pattern initial value
            if (patterns) {
                this.setState({ pattern: Object.values(patterns)[0] })
            }
        }).catch(error => {
            if (error.response && error.response.status === 401) {
                window.location = "/login"; // api key has expired
            } else {
                console.log(error);
            }
        });

        axios.get("/api/user/data", authConfig).then(response => {
            const colors = response.data["colors"];
            const colorLists = response.data["color_lists"];

            this.setState({ colors: colors, colorLists: colorLists });

            // set initial values
            if (colors) {
                this.setState({ color: Object.values(colors)[0] })
            }
            if (colorLists) {
                this.setState({ selectedColorList: Object.values(colorLists)[0] })
            }
        }).catch(error => {
            if (error.response && error.response.status === 401) {
                window.location = "/login"; // api key has expired
            } else {
                console.log(error);
            }
        });
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
                                    color={this.state.color}
                                    onChange={e => this.setState({ color: e.hex })}/>
                            </Popover>
                        </Overlay>
                        <Form.Control ref="colorField"
                                      type="text"
                                      placeholder="#RRGGBB"
                                      value={this.state.color}
                                      onChange={e => this.setState({ color: e.target.value })}
                                      disabled={!this.state.customColor}/>
                    </Form.Group>
                </Form.Row>

                <Form.Row>
                    <Form.Group controlId="customColorCheck">
                        <Form.Check value={this.state.customColor}
                                    onChange={this.handleCustomColorCheck}
                                    label="Custom color"/>
                    </Form.Group>

                    // TODO: Align right
                    <Form.Group controlId="saveButton">
                        <Button variant="success" onClick={this.handleSave}>
                            Save
                        </Button>
                    </Form.Group>
                </Form.Row>
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
        switch (this.state.pattern) {
            case "fade":
            case "scroll":
            case "stripes":
                config = colorListEntry;
                break;
            case "solid_color":
                config = colorEntry;
                break;
        }

        return (
            <Form onSubmit={this.handleSubmit}>
                <Form.Group controlId="patternSelect">
                    <Form.Label>Pattern</Form.Label>
                    <Form.Control as="select"
                                  onChange={e => this.setState({ pattern: e.target.value })}>
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
        this.setState({
            selectedColor: event.target.value,
            color: this.state.colors[event.target.value]
        });
    };

    /**
     * Update the currently entered color list based on a select change event.
     * @param event - The change event from the select
     */
    handleColorListSelect = (event) => {
        this.setState({
            selectedColorList: event.target.value,
            colorList: this.state.colorLists[event.target.value]
        });
    };

    /**
     * Change whether the user can type the hex of a custom color or select from
     * the list of saved colors.
     * @param event - The change event from the checkbox
     */
    handleCustomColorCheck = (event) => {
        this.setState({ customColor: event.target.checked });

        if (!event.target.checked) {
            this.setState({ color: this.state.colors[this.state.selectedColor] })
        }
    };

    /**
     * Save the current custom color or color_List for the logged-in user.
     * @param event - The save event
     */
    handleSave = (event) => {
        // TODO: Implement save
    };

    /**
     * Submit the form data.
     * @param event - The submit event
     */
    handleSubmit = (event) => {
        event.preventDefault();

        const target = event.currentTarget;  // TODO: Use only state if possible

        // data fields
        let pattern, strobe, color, colorList;

        pattern = target["patternSelect"].value;
        strobe = this.state.strobe;

        // TODO: Synchronize state to not need any logic in this method
        // set color field
        if (target["colorField"] && this.state.customColor) {
            color = target["colorField"].value;
        } else if (target["colorSelect"]) {
            color = this.state.colors[target["colorSelect"].value];
        }

        // set color_list field
        if (target["colorListSelect"]) {
            colorList = this.state.colorLists[target["colorListSelect"].value];
        }

        const data = {
            "client_id": this.props.clientId,
            "pattern": pattern,
            "strobe": strobe,
            "color": color,
            "color_list": colorList
        };

        this.submit(data);
    };

    /**
     * Submit a request to turn off the lights.
     * @param event - The "Turn off" button event
     */
    handleOff = (event) => {
        event.preventDefault();

        const data = {
            "client_id": this.props.clientId,
            "pattern": "off"
        };

        this.submit(data);
    };

    /**
     * Submit data to the Webcandy API to run a lighting configuration. Valid
     * fields for data are described in the submit route documentation
     * (submit method in routes.py).
     * @param data - The lighting pattern and settings to run
     */
    submit(data) {
        axios.post("/api/submit", data, getAuthConfig())
            .then(response => console.log(response))
            .catch(error => {
                if (error.response.status === 401) {
                    window.location = "/login"; // unauthorized
                } else {
                    console.log(error);
                }
            });
    }
}

LightConfigForm.propTypes = {
    clientId: PropTypes.string.isRequired,
};
