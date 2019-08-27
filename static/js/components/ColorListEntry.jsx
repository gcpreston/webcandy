import React from 'react';
import PropTypes from 'prop-types';
import { Col, Form, Button } from "react-bootstrap";
import ColorEntry from "./ColorEntry";

/**
 * Form component for editing and saving a color list.
 */
export default class ColorListEntry extends React.Component {
    static propTypes = {
        colors: PropTypes.arrayOf(PropTypes.string), // array of hexes
        selectedIndex: PropTypes.number,
        editingColor: PropTypes.string,
        buttonDisabled: PropTypes.bool,
        buttonText: PropTypes.string,
        buttonVariant: PropTypes.string,
        onChange: PropTypes.func, // on color edit
        onSelect: PropTypes.func,
        onButtonClick: PropTypes.func, // color entry button action
        onNewColor: PropTypes.func,
        onDeleteColor: PropTypes.func,
        className: PropTypes.string
    };

    /**
     * INVARIANT: Color entry is disabled if there is no color selected.
     */
    entryIsDisabled() {
        return this.props.colors.length === 0
            || this.props.selectedIndex === -1;
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
                                  value={[this.props.selectedIndex]}
                                  onChange={this.props.onSelect}>
                        {this.props.colors.map((color, idx) => {
                            return <option key={idx}
                                           value={idx}>{color}</option>;
                        })}
                    </Form.Control>
                </Form.Group>
                <Form.Group as={Col} controlId="colorListEditField">
                    <ColorEntry
                        color={this.props.editingColor}
                        textDisabled={this.entryIsDisabled()}
                        buttonDisabled={this.props.buttonDisabled}
                        buttonText={this.props.buttonText}
                        buttonVariant={this.props.buttonVariant}
                        onChange={this.props.onChange}
                        onButtonClick={this.props.onButtonClick}
                    />
                    <Button variant="link" onClick={this.props.onNewColor}>
                        New color
                    </Button>
                    <Button variant="link" onClick={this.props.onDeleteColor}>
                        Delete color
                    </Button>
                </Form.Group>
            </Form.Row>
        );
    }
}
