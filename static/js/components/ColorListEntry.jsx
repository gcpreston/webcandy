import React from 'react';
import PropTypes from 'prop-types';
import { Col, Form } from "react-bootstrap";
import ColorEntry from "./ColorEntry";

/**
 * Form component for editing and saving a color list.
 */
export default class ColorListEntry extends React.Component {
    static propTypes = {
        buttonText: PropTypes.string, // color entry button text
        colors: PropTypes.arrayOf(PropTypes.string), // array of hexes
        selectedColor: PropTypes.string, // hex
        editingColor: PropTypes.string, // hex
        onColorSelectChange: PropTypes.func,
        onColorEdit: PropTypes.func,
        onButtonClick: PropTypes.func // color entry button action
    };

    static defaultProps = {
        buttonText: "",
        selectedColorList: "",
        selectedColor: "",
        editingColor: ""
    };

    render() {
        return (
            <Form.Row>
                <Form.Group as={Col} controlId="colorListValueDisplay">
                    <Form.Control as="select" multiple
                                  value={[this.props.selectedColor]}
                                  onChange={this.props.onColorSelectChange}>
                        {this.props.colors.map((color, idx) => {
                            return <option key={idx}>{color}</option>;
                        })}
                    </Form.Control>
                </Form.Group>
                <Form.Group as={Col} controlId="colorListEditField">
                    <ColorEntry color={this.props.editingColor}
                                buttonText={this.props.buttonText}
                                overlayTrigger="focus"
                                onChange={this.props.onColorEdit}
                                onButtonClick={this.props.onButtonClick}/>
                </Form.Group>
            </Form.Row>
        );
    }
}
