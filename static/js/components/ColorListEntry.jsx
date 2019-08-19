import React from 'react';
import PropTypes from 'prop-types';
import { Col, Form } from "react-bootstrap";
import ColorEntry from "./ColorEntry";

/**
 * Form component for editing and saving a color list.
 */
export default class ColorListEntry extends React.Component {
    static propTypes = {
        colors: PropTypes.arrayOf(PropTypes.string), // array of hexes
        onChange: PropTypes.func,
        onButtonClick: PropTypes.func // color entry button action
    };

    state = {
        selectedIndex: -1,
        editingColor: ""
    };

    render() {
        return (
            <Form.Row>
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
                        buttonText="Save"
                        onChange={this.handleColorEdit}
                        onButtonClick={this.props.onButtonClick}
                    />
                </Form.Group>
            </Form.Row>
        );
    }

    handleColorSelect = (event) => {
        const idx = Number(event.target.value);
        this.setState({
            selectedIndex: idx,
            editingColor: this.props.colors[idx]
        });
    };

    /**
     * Handle ColorEntry's onChange event. Send the edited color list to the
     * given onChange function.
     */
    handleColorEdit = (color) => {
        this.setState({ editingColor: color });

        let newColors = this.props.colors.slice();
        newColors[this.state.selectedIndex] = color;
        this.props.onChange(newColors);
    };
}
