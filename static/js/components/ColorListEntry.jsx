import React from 'react';
import PropTypes from 'prop-types';
import { Col, Form, Button } from "react-bootstrap";
import ColorEntry from "./ColorEntry";

/**
 * Form component for editing and saving a color list.
 */
export default class ColorListEntry extends React.Component {
    static propTypes = {
        buttonText: PropTypes.string,
        buttonVariant: PropTypes.string,
        colors: PropTypes.arrayOf(PropTypes.string), // array of hexes
        onChange: PropTypes.func,
        onButtonClick: PropTypes.func, // color entry button action
        className: PropTypes.string
    };

    state = {
        selectedIndex: -1,
        editingColor: "",
    };

    /**
     * INVARIANT: Logic to determine whether or not color entry is disabled
     * based on state.
     */
    entryIsDisabled() {
        return this.props.colors.length === 0
            || this.state.selectedIndex === -1;
    }

    render() {
        let className = "color-list-entry";
        if (this.props.className) {
            className += ` ${this.props.className}`;
        }

        // TODO: Add ability to change color order
        return (
            <Form.Row className={className}>
                <Form.Group as={Col} controlId="colorListValueDisplay">
                    <Form.Control as="select" multiple
                                  value={[this.state.selectedIndex]}
                                  onChange={this.handleColorSelect}>
                        {this.props.colors.map((color, idx) => {
                            return <option key={idx}
                                           value={idx}>{color}</option>;
                        })}
                    </Form.Control>
                </Form.Group>
                <Form.Group as={Col} controlId="colorListEditField">
                    <ColorEntry
                        color={this.state.editingColor}
                        disabled={this.entryIsDisabled()}
                        buttonText={this.props.buttonText}
                        buttonVariant={this.props.buttonVariant}
                        onChange={this.handleColorEdit}
                        onButtonClick={this.props.onButtonClick}
                    />
                    <Button variant="link" onClick={this.handleNewColor}>
                        New color
                    </Button>
                    <Button variant="link" onClick={this.handleDeleteColor}>
                        Delete color
                    </Button>
                </Form.Group>
            </Form.Row>
        );
    }

    /**
     * Handle a different color being selected from the list of entered colors.
     */
    handleColorSelect = (event) => {
        let newSelectedIndex = Number(event.target.value);
        let newEditingColor = this.props.colors[newSelectedIndex];

        if (event.target.value === "") {
            newSelectedIndex = -1;
            newEditingColor = ""
        }

        this.setState({
            selectedIndex: newSelectedIndex,
            editingColor: newEditingColor,
        });
    };

    /**
     * Handle ColorEntry's onChange event. Send the edited color list to the
     * given onChange function.
     */
    handleColorEdit = (event) => {
        this.setState({ editingColor: event.color });

        let newColors = this.props.colors.slice();
        newColors[this.state.selectedIndex] = event.color;
        this.props.onChange({ colorList: newColors });
    };

    /**
     * Handle the "New color" button being pressed. Add an empty string to the
     * color list and invoke props.onChange.
     */
    handleNewColor = () => {
        const newColors = this.props.colors.slice();
        let newSelectedIndex = this.state.selectedIndex;

        if (this.state.selectedIndex >= 0 &&
            this.state.selectedIndex < this.props.colors.length) {
            newSelectedIndex = this.state.selectedIndex + 1;
            newColors.splice(newSelectedIndex, 0, "");
        } else {
            newColors.push("");
            newSelectedIndex = this.props.colors.length;
        }

        this.setState({
            selectedIndex: newSelectedIndex,
            editingColor: "",
            entryDisabled: false
        });

        this.props.onChange({ colorList: newColors });
    };

    /**
     * Handle the "Delete color" button being pressed. Remove the currently
     * selected color from the color list and invoke props.onChange.
     */
    handleDeleteColor = () => {
        const newColors = this.props.colors.slice();
        let newSelectedIndex = this.state.selectedIndex;
        let newEditingColor = this.state.editingColor;

        if (this.state.selectedIndex >= 0 &&
            this.state.selectedIndex < this.props.colors.length) {
            // delete element at selected index
            newColors.splice(this.state.selectedIndex, 1);

            // Keep same selected index, unless it was the last one, in which
            // case make it the new last index.
            // newColors.length = 0 -> newSelectedIndex = -1, which is correct
            if (this.state.selectedIndex === newColors.length) {
                newSelectedIndex -= 1;
            }

            if (newColors.length === 0) {
                newEditingColor = "";
            } else {
                newEditingColor = newColors[newSelectedIndex];
            }
        }

        this.setState({
            selectedIndex: newSelectedIndex,
            editingColor: newEditingColor
        });

        this.props.onChange({ colorList: newColors });
    };
}
