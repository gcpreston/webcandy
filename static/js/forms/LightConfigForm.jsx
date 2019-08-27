import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios/index';
import {
    Button,
    Col,
    Form,
} from 'react-bootstrap';
import Dialog from 'react-bootstrap-dialog';
import ReactBootstrapSlider from 'react-bootstrap-slider';

import ColorEntry from "../components/ColorEntry";
import ColorListEntry from "../components/ColorListEntry";
import {
    getAuthConfig,
    getMatchingObject,
    getMatchingIndex,
} from '../util.js';

import "bootstrap-slider/dist/css/bootstrap-slider.css"
import { arraysEqual } from "../util";

/**
 * Form for building lighting configuration request.
 */
export default class LightConfigForm extends React.Component {
    // this.dialog will be set later for prompting the user
    dialog = null;

    // TODO: Add some kind of loading flag so "No clients connected" does
    //   not pop up momentarily before loading data
    state = {
        patterns: [],
        offButton: false,  // display "Turn off" button if "Off" pattern exists
        pattern: null,
        // color select/entry
        colors: {},
        enteredColor: "",  // hex
        selectedColor: "",  // name of color
        // color list select/entry
        colorLists: {},
        selectedColorList: "",  // name of color list
        enteredColorList: [],  // hex list
        selectedColorListIndex: -1, // nothing selected by default
        editingColor: "",  // hex
        // extra params for submission
        strobe: false,
        speed: 5.0
    };

    // ------------------------------
    // Invariants computed from state
    // ------------------------------

    /**
     * Get the current color based on if the current pattern utilizes the color
     * field and if a custom color is entered.
     */
    getCurrentColor() {
        if (this.state.pattern["takes"] === "color") {
            const selected = this.state.colors[this.state.selectedColor];
            if (this.state.enteredColor !== selected) {
                return this.state.enteredColor;
            }
            return selected;
        }
        return null;
    }

    /**
     * Get the current color list based on if the current pattern utilitzes
     * the color_list field.
     */
    getCurrentColorList() {
        if (this.state.pattern["takes"] === "color_list") {
            return this.state.enteredColorList;
        }
        return null;
    }

    /**
     * Get the current speed based on if the current pattern is static or
     * dynamic.
     */
    getCurrentSpeed() {
        if (this.state.pattern["type"] === "dynamic") {
            return this.state.speed;
        }
        return null;
    }

    /**
     * Determine whether the current color list has been edited from the latest
     * saved version.
     */
    colorListHasBeenEdited() {
        return !arraysEqual(this.state.enteredColorList,
            this.state.colorLists[this.state.selectedColorList])
    }

    // ---------------
    // Component logic
    // ---------------

    /**
     * Get values from Webcandy API and set state before app renders.
     */
    componentWillMount() {
        this.updatePatterns();
        this.updateSavedData();
    }

    /**
     * Get the latest patterns the client has access to and store them in state.
     */
    updatePatterns() {
        const clientConfig = getAuthConfig();
        clientConfig["params"] = { "client_id": this.props.clientId };

        axios.get("/api/user/clients", clientConfig).then(response => {
            let patterns = response.data.patterns;

            // remove "Off" from patterns so it doesn't appear on the dropdown
            const index = getMatchingIndex(patterns, "name", "Off");
            let offButtonVal = false;
            if (index > -1) {
                patterns.splice(index, 1);
                offButtonVal = true;
            }

            this.setState({
                patterns: patterns,
                pattern: patterns ? patterns[0] : "",
                offButton: offButtonVal,
            });
        }).catch(error => {
            if (error.response && error.response.status === 401) {
                // api key has expired; redirect to login page
                window.location = "/login";
            } else {
                console.log(error);
            }
        });
    }

    /**
     * Get the latest saved data of the current user and store it in state.
     */
    updateSavedData(reset = false) {
        axios.get("/api/user/data", getAuthConfig()).then(response => {
            const colors = response.data["colors"];
            const colorLists = response.data["color_lists"];

            this.setState({ colors: colors, colorLists: colorLists });

            // set or reset initial values
            if (colors && (reset || !this.state.selectedColor)) {
                this.setState({
                    selectedColor: Object.keys(colors)[0],
                    enteredColor: Object.values(colors)[0]
                })
            }
            if (colorLists && (reset || !this.state.selectedColorList)) {
                this.setState({
                    selectedColorList: Object.keys(colorLists)[0],
                    enteredColorList: Object.values(colorLists)[0],
                    selectedColorListIndex: -1,
                    editingColor: ""
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

    render() {
        const colorEntry = (
            <React.Fragment>
                <Form.Label>Color entry</Form.Label>
                <Form.Row>
                    <Form.Group as={Col} controlId="colorSelect">
                        <Form.Control as="select"
                                      value={this.state.selectedColor}
                                      onChange={this.handleColorSelect}>
                            {Object.keys(this.state.colors).map((name, idx) => {
                                return <option
                                    key={idx}>{name}</option>;
                            })}
                        </Form.Control>
                    </Form.Group>
                    <Form.Group as={Col} controlId="colorField">
                        <ColorEntry color={this.state.enteredColor}
                                    buttonText="Save"
                                    onChange={e => this.setState({ enteredColor: e.color })}
                                    onButtonClick={this.colorSavePrompt}/>
                    </Form.Group>
                </Form.Row>
            </React.Fragment>
        );

        const colorListEntry = (
            <React.Fragment>
                <Form.Label>Color list entry</Form.Label>
                <Button variant="link" onClick={this.newColorListPrompt}>
                    New
                </Button>
                <Button variant="link" onClick={this.deleteColorListPrompt}>
                    Delete
                </Button>
                <Form.Group controlId="colorListSelect">
                    <Form.Control as="select"
                                  value={this.state.selectedColorList}
                                  onChange={this.handleColorListSelect}>
                        {Object.keys(this.state.colorLists).map((name, idx) => {
                            return <option key={idx}>{name}</option>;
                        })}
                    </Form.Control>
                </Form.Group>
                <ColorListEntry
                    colors={this.state.enteredColorList}
                    editingColor={this.state.editingColor}
                    selectedIndex={this.state.selectedColorListIndex}
                    buttonDisabled={!this.colorListHasBeenEdited()}
                    onSelect={this.handleColorListValueSelect}
                    onChange={this.handleColorListChange}
                    onButtonClick={() => {
                            this.saveColorList(this.state.selectedColorList,
                                this.state.enteredColorList)
                        }}
                    onNewColor={this.handleNewColor}
                    onDeleteColor={this.handleDeleteColor}
                />
            </React.Fragment>
        );

        // Set config based on if color or color_list needs to be entered
        let config;
        if (this.state.pattern) {
            if (this.state.pattern["takes"] === "color") {
                config = colorEntry;
            } else if (this.state.pattern["takes"] === "color_list") {
                config = colorListEntry;
            }
        }

        // Add speed slider if dynamic pattern
        if (this.state.pattern && this.state.pattern["type"] === "dynamic") {
            config = (
                <React.Fragment>
                    {config}

                    <Form.Row>
                        <Form.Group as={Col} controlId="speedSlider">
                            <Form.Label>Speed: {Number(this.state.speed).toFixed(1)}</Form.Label>
                            <br/>
                            <ReactBootstrapSlider
                                value={this.state.speed}
                                change={e => this.setState({ speed: Number(e.target.value) })}
                                step={0.1}
                                max={20}
                                min={0}/>
                        </Form.Group>
                    </Form.Row>
                </React.Fragment>
            )
        }

        return (
            <React.Fragment>
                <Dialog ref={component => this.dialog = component}/>

                <Form onSubmit={this.handleSubmit}>
                    <Form.Group controlId="patternSelect">
                        <Form.Label>Pattern</Form.Label>
                        <Form.Control as="select"
                                      onChange={this.handlePatternSelect}>
                            {this.state.patterns.map((p, idx) => {
                                return <option key={idx}>{p.name}</option>;
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
            </React.Fragment>
        );
    }

    colorSavePrompt = () => {
        if (Object.values(this.state.colors).includes(this.state.enteredColor)) {
            this.dialog.show({
                title: "Info",
                body: "The color " + this.state.enteredColor + " is already saved.",
                actions: [
                    Dialog.DefaultAction(
                        "OK",
                        () => {
                        },
                        "btn-info"
                    )
                ]
            });
        } else {
            this.dialog.show({
                title: "Save Color",
                body: "Enter a name for this color:",
                prompt: Dialog.TextPrompt({ placeholder: "Name" }),
                actions: [
                    Dialog.CancelAction(),
                    Dialog.OKAction(dialog => {
                        const colorName = dialog.value;
                        if (Object.keys(this.state.colors).includes(colorName)) {

                            this.dialog.show({
                                title: "Confirmation",
                                body: 'Would you like to overwrite the existing "'
                                    + colorName + '" color? ('
                                    + this.state.colors[colorName] + ')',
                                actions: [
                                    Dialog.CancelAction(),
                                    Dialog.DefaultAction(
                                        "Overwrite",
                                        () => this.saveColor(colorName, this.state.enteredColor),
                                        "btn-warning"
                                    )
                                ]
                            });

                        } else {
                            this.saveColor(dialog.value, this.state.enteredColor);
                        }
                    })
                ]
            });
        }
    };

    newColorListPrompt = () => {
        this.dialog.show({
            title: "New Color List",
            prompt: Dialog.TextPrompt({ placeholder: "Name" }),
            actions: [
                Dialog.CancelAction(),
                Dialog.DefaultAction(
                    "Create",
                    dialog => {
                        const colorListName = dialog.value;
                        if (Object.keys(this.state.colorLists).includes(colorListName)) {

                            this.dialog.show({
                                title: "Error",
                                body: 'A color list named "' + colorListName +
                                    '" already exists. Delete this color list ' +
                                    'if you would like to overwrite it.',
                                actions: [
                                    Dialog.OKAction()
                                ]
                            });

                        } else {
                            const newColorLists = Object.assign(this.state.colorLists);
                            newColorLists[colorListName] = [];
                            this.setState({
                                colorLists: newColorLists,
                                selectedColorList: colorListName,
                                enteredColorList: newColorLists[colorListName],
                                selectedColorListIndex: -1,
                                editingColor: ""
                            });
                        }
                    },
                    "btn-success")
            ]
        });
    };

    deleteColorListPrompt = () => {
        this.dialog.show({
            title: "Delete Color List",
            body: 'Are you sure you want to delete the "' +
                this.state.selectedColorList + '" color list? This action ' +
                'cannot be undone.',
            actions: [
                Dialog.CancelAction(),
                Dialog.DefaultAction(
                    "Delete",
                    () => {
                        const config = getAuthConfig();
                        config.data = { "color_lists": [this.state.selectedColorList] };
                        axios.delete("/api/user/data", config)
                            .then(response => {
                                console.log(response.data);
                                this.updateSavedData(true);
                            })
                            .catch(error => console.log(error));
                    },
                    "btn-danger"
                )
            ]
        });
    };

    /**
     * Save the current custom color for the logged-in user.
     * @param name - The name to save the color as
     * @param color - The hex value to save
     */
    saveColor = (name, color) => {
        const data = {
            "colors": {
                [name]: color
            }
        };
        this.saveData(data);
    };

    /**
     * Save the current custom color list for the logged-in user.
     * @param name - The name to save the color list as
     * @param colorList - The list of hex values to save
     */
    saveColorList = (name, colorList) => {
        const data = {
            "color_lists": {
                [name]: colorList
            }
        };
        this.saveData(data);
    };

    /**
     * Save data for the logged-in user.
     */
    saveData(data) {
        axios.put("/api/user/data", data, getAuthConfig())
            .then(response => {
                console.log(response);
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
    }

    handlePatternSelect = (event) => {
        const pattern = getMatchingObject(
            this.state.patterns, "name", event.target.value);

        let speed = this.state.speed;
        if (pattern.hasOwnProperty("default_speed"))
            speed = pattern["default_speed"];

        this.setState({
            pattern: pattern,
            speed: speed
        })
    };

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
        const colorList = this.state.colorLists[event.target.value];
        this.setState({
            selectedColorList: event.target.value,
            enteredColorList: colorList,
            selectedColorListIndex: -1,
            editingColor: ""
        });
    };

    /**
     * Handle a different color being selected from the list of entered colors.
     * @param event - The change event from the select
     */
    handleColorListValueSelect = (event) => {
        let newSelectedIndex = Number(event.target.value);
        let newEditingColor = this.state.enteredColorList[newSelectedIndex];

        if (event.target.value === "") {
            newSelectedIndex = -1;
            newEditingColor = ""
        }

        this.setState({
            selectedColorListIndex: newSelectedIndex,
            editingColor: newEditingColor,
        });
    };

    /**
     * Handle ColorListEntry's onChange event. Update the color list in state
     * with the edited value.
     */
    handleColorListChange = (event) => {
        this.setState({ editingColor: event.color });

        let newColors = this.state.enteredColorList.slice();
        newColors[this.state.selectedColorListIndex] = event.color;
        this.setState({ enteredColorList: newColors });
    };

    /**
     * Handle ColorListEntry's "New color" button being pressed. Add an empty
     * string to the color list.
     */
    handleNewColor = () => {
        const newColors = this.state.enteredColorList.slice();
        let newSelectedIndex = this.state.selectedColorListIndex;

        // color selected -> new color after selected
        // no color selected -> new color at the front
        if (newSelectedIndex >= 0 &&
            newSelectedIndex < newColors.length) {
            newSelectedIndex +=  1;
            newColors.splice(newSelectedIndex, 0, "");
        } else {
            // newSelectedIndex should only be -1
            newColors.splice(0, 0, ""); // push to front of list
            newSelectedIndex = 0;
        }

        this.setState({
            enteredColorList: newColors,
            selectedColorListIndex: newSelectedIndex,
            editingColor: "",
        });
    };

    /**
     * Handle the "Delete color" button being pressed. Remove the currently
     * selected color from the color list.
     */
    handleDeleteColor = () => {
        const newColors = this.state.enteredColorList.slice();
        let newSelectedIndex = this.state.selectedColorListIndex;
        let newEditingColor = this.state.editingColor;

        // color must be selected for one to be deleted
        if (newSelectedIndex >= 0 &&
            newSelectedIndex < newColors.length) {
            // delete element at selected index
            newColors.splice(newSelectedIndex, 1);

            // select element before deleted one
            newSelectedIndex -= 1;

            // index of -1 indicates that nothing is selected
            if (newSelectedIndex === -1) {
                newEditingColor = "";
            } else {
                newEditingColor = newColors[newSelectedIndex];
            }
        }

        this.setState({
            enteredColorList: newColors,
            selectedColorListIndex: newSelectedIndex,
            editingColor: newEditingColor
        });
    };

    /**
     * Submit the form data.
     * @param event - The submit event
     */
    handleSubmit = (event) => {
        event.preventDefault();

        const data = {
            "client_id": this.props.clientId,
            "pattern": this.state.pattern.name,
            "strobe": this.state.strobe,
        };

        const currentColor = this.getCurrentColor();
        if (currentColor) {
            data["color"] = currentColor;
        }

        const currentColorList = this.getCurrentColorList();
        if (currentColorList) {
            data["color_list"] = currentColorList;
        }

        const currentSpeed = this.getCurrentSpeed();
        if (currentSpeed) {
            data["speed"] = currentSpeed;
        }

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
            "pattern": "Off"
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
