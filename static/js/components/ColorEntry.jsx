import React from 'react';
import PropTypes from 'prop-types';
import {
    Button,
    Form,
    InputGroup,
    OverlayTrigger,
    Popover
} from "react-bootstrap";
import ChromePicker from "react-color";

/**
 * Form control allowing user to enter a #RRGGBB color using a color picker.
 */
export default class ColorEntry extends React.Component {
    static propTypes = {
        color: PropTypes.string, // format #RRGGBB
        buttonText: PropTypes.string,
        overlayTrigger: PropTypes.string, // OverlayTrigger "trigger" prop
        overlayPlacement: PropTypes.string, // OverlayTrigger "placement" prop
        onChange: PropTypes.func, // on color change
        onButtonClick: PropTypes.func
    };

    // TODO: Don't show color entry when button is clicked
    render() {
        return (
            <OverlayTrigger
                trigger={this.props.overlayTrigger}
                placement={this.props.overlayPlacement}
                overlay={
                    <Popover>
                        <ChromePicker
                            color={this.props.color}
                            onChange={this.handlePickerChange}/>
                    </Popover>
                }>
                <InputGroup ref="colorField">
                    <Form.Control type="text"
                                  placeholder="#RRGGBB"
                                  value={this.props.color}
                                  onChange={this.handleFieldChange}/>
                    <InputGroup.Append>
                        <Button variant="success"
                                onClick={this.props.onButtonClick}>
                            {this.props.buttonText}
                        </Button>
                    </InputGroup.Append>
                </InputGroup>
            </OverlayTrigger>
        );
    }

    handlePickerChange = (event) => {
        return this.props.onChange(event.hex);
    };

    handleFieldChange = (event) => {
        return this.props.onChange(event.target.value);
    };
}
