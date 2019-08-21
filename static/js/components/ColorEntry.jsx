import React from 'react';
import PropTypes from 'prop-types';
import {
    Button,
    Form,
    InputGroup,
    Overlay,
    Popover
} from "react-bootstrap";
import ChromePicker from "react-color";

/**
 * Form control allowing user to enter a #RRGGBB color using a color picker.
 */
export default class ColorEntry extends React.Component {
    static propTypes = {
        color: PropTypes.string, // format #RRGGBB
        buttonVariant: PropTypes.string,
        buttonText: PropTypes.string,
        overlayPlacement: PropTypes.string, // Overlay "placement" prop
        onChange: PropTypes.func, // on color change
        onButtonClick: PropTypes.func,
        className: PropTypes.string
    };

    static defaultProps = {
        buttonVariant: "success"
    };

    // use state to determine whether a custom color is entered to avoid
    // OverlayTrigger showing the popup when the button is focused and
    // not the text field
    state = {
        customColor: false
    };

    render() {
        let className = "color-entry";
        if (this.props.className) {
            className = ` ${this.props.className}`;
        }

        return (
            <div className={className}>
                <Overlay target={this.refs.colorField}
                         show={this.state.customColor}
                         placement={this.props.overlayPlacement}>
                    <Popover>
                        <ChromePicker
                            color={this.props.color}
                            onChange={this.handlePickerChange}
                        />
                    </Popover>
                </Overlay>
                <InputGroup ref="colorField">
                    <Form.Control
                        type="text"
                        placeholder="#RRGGBB"
                        value={this.props.color}
                        onChange={this.handleFieldChange}
                        onFocus={() => this.setState({ customColor: true })}
                        onBlur={() => this.setState({ customColor: false })}
                    />
                    <InputGroup.Append>
                        <Button variant={this.props.buttonVariant}
                                onClick={this.props.onButtonClick}>
                            {this.props.buttonText}
                        </Button>
                    </InputGroup.Append>
                </InputGroup>
            </div>
        );
    }

    // TODO: Pass an event object with a "color" field rather than just the
    //   color variable to props.onChange
    handlePickerChange = (event) => {
        return this.props.onChange(event.hex);
    };

    handleFieldChange = (event) => {
        return this.props.onChange(event.target.value);
    };
}
