import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios/index';
import ChromePicker from 'react-color';
import {
    Button,
    Col,
    Form,
    InputGroup,
    Overlay,
    Popover,
    Modal
} from 'react-bootstrap';
import { getAuthConfig } from '../../util.js';

let colorPatterns = ["solid_color"];
let colorListPatterns = ["fade", "scroll", "stripes"];

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
            enteredColor: "",  // hex
            selectedColor: "",  // name of color
            customColor: false,
            colorLists: {},
            enteredColorList: [],  // hex list
            selectedColorList: "",  // name of color list
            strobe: false,
            saveModalShow: false,
            saveModalName: ""
        };
    }

    /**
     * Get the current color based on if the current pattern utilizes the color
     * field and if the "Custom color" checkbox is selected.
     */
    getCurrentColor() {
        if (colorPatterns.includes(this.state.pattern)) {
            if (this.state.customColor) {
                return this.state.enteredColor;
            }
            return this.state.colors[this.state.selectedColor];
        }
        return null;
    }

    /**
     * Get the current color list basedo n if the current pattern utilitzes
     * the color_list field
     */
    getCurrentColorList() {
        if (colorListPatterns.includes(this.state.pattern)) {
            // TODO: Update this logic when color list entry is implemented
            return this.state.colorLists[this.state.selectedColorList];
        }
        return null;
    }

    /**
     * Get values from Webcandy API and set state before app renders.
     */
    componentWillMount() {
        this.updatePatterns();
        this.updateSavedData();
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
                                      value={this.state.selectedColor}
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
                                    color={this.state.enteredColor}
                                    onChange={e => this.setState({ enteredColor: e.hex })}/>
                            </Popover>
                        </Overlay>
                        <InputGroup ref="colorField">
                            <Form.Control type="text"
                                          placeholder="#RRGGBB"
                                          value={this.state.enteredColor}
                                          onChange={e => this.setState({ enteredColor: e.target.value })}
                                          disabled={!this.state.customColor}/>
                            <InputGroup.Append>
                                <Button variant="success"
                                        disabled={!this.state.customColor}
                                        onClick={() => this.setState({ saveModalShow: true })}>
                                    Save
                                </Button>
                            </InputGroup.Append>
                        </InputGroup>
                    </Form.Group>
                </Form.Row>

                <Form.Group controlId="customColorCheck">
                    <Form.Check value={this.state.customColor}
                                onChange={this.handleCustomColorCheck}
                                label="Custom color"/>
                </Form.Group>

                <Modal show={this.state.saveModalShow}
                       size="sm"
                       centered
                       className="text-dark">
                    <Modal.Header>
                        <Modal.Title>Save Color</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form onSubmit={this.handleSaveColor}>
                            <Form.Group controlId="name">
                                <Form.Label>Enter a name for this color</Form.Label>
                                <Form.Control type="text"
                                              placeholder="Name"
                                              value={this.state.saveModalName}
                                              onChange={e => this.setState({ saveModalName: e.target.value })}/>
                            </Form.Group>
                        </Form>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary"
                                onClick={() => this.setState({ saveModalShow: false })}>
                            Cancel
                        </Button>
                        <Button variant="primary"
                                onClick={this.handleSaveColor}>
                            Save
                        </Button>
                    </Modal.Footer>
                </Modal>
            </React.Fragment>
        );

        let colorListEntry = (
            <Form.Row>
                <Form.Group as={Col} controlId="colorListSelect">
                    <Form.Label>Color list entry</Form.Label>
                    <Form.Control as="select"
                                  value={this.state.selectedColorList}
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
                // this.setState({ enteredColor: "" });
                break;
            case "solid_color":
                config = colorEntry;
                // this.setState({ enteredColorList: [] });
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
     * Get the latest patterns the client has access to and store them in state.
     */
    updatePatterns() {
        const clientConfig = getAuthConfig();
        clientConfig["params"] = { "client_id": this.props.clientId };

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

    }

    /**
     * Get the latest saved data of the current user and store it in state.
     */
    updateSavedData() {
        axios.get("/api/user/data", getAuthConfig()).then(response => {
            const colors = response.data["colors"];
            const colorLists = response.data["color_lists"];

            this.setState({ colors: colors, colorLists: colorLists });

            // set initial values
            if (colors && !this.state.selectedColor) {
                this.setState({
                    selectedColor: Object.keys(colors)[0],
                    enteredColor: Object.values(colors)[0]
                })
            }
            if (colorLists && !this.state.selectedColorList) {
                this.setState({
                    selectedColorList: Object.keys(colorLists)[0],
                    enteredColorList: Object.values(colorLists)[0]
                })
            }
        }).catch(error => {
            if (error.response && error.response.status === 401) {
                window.location = "/login"; // api key has expired
            } else {
                console.log(error);
            }
        });
    }

    /**
     * Update the currently entered color based on a select change event.
     * @param event - The change event from the select
     */
    handleColorSelect = (event) => {
        this.setState({
            selectedColor: event.target.value,
            enteredColor: this.state.colors[event.target.value]
        });
    };

    /**
     * Update the currently entered color list based on a select change event.
     * @param event - The change event from the select
     */
    handleColorListSelect = (event) => {
        this.setState({
            selectedColorList: event.target.value,
            enteredColorList: this.state.colorLists[event.target.value]
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
            this.setState({ enteredColor: this.state.colors[this.state.selectedColor] })
        }
    };

    /**
     * Save the current custom color for the logged-in user.
     * @param event - The save event
     */
    handleSaveColor = (event) => {
        event.preventDefault();

        const name = this.state.saveModalName;
        const data = {
            "colors": {
                [name]: this.state.enteredColor
            }
        };

        this.setState({ saveModalShow: false, saveModalName: "" });

        axios.put("/api/user/data", data, getAuthConfig())
            .then(() => {
                this.updateSavedData();
                this.setState({ selectedColor: name })

            })
            .catch(error => {
                if (error.response.status === 401) {
                    window.location = "/login"; // unauthorized
                } else {
                    console.log(error);
                }
            });
    };

    /**
     * Submit the form data.
     * @param event - The submit event
     */
    handleSubmit = (event) => {
        event.preventDefault();

        const data = {
            "pattern": this.state.pattern,
            "strobe": this.state.strobe,
            "color": this.getCurrentColor(),
            "color_list": this.getCurrentColorList()
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
