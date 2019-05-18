import React, { Component } from "react";
import axios from "axios";
import ChromePicker from "react-color";
import { Button, Form, Overlay, Popover } from "react-bootstrap";

export default class FadecandyForm extends Component {
  constructor(props) {
    super(props);

    this.state = {
      configs: [],
      colors: {},
      solidColor: false,
      customColor: false,
      currentColor: ""
    };
  }

  /**
   * Get values from Webcandy API and set state before app renders.
   */
  componentWillMount() {
    axios.get("/configs").then(response => {
      this.setState({ configs: response.data });
    });

    axios.get("/colors").then(response => {
      let colors = response.data;
      this.setState({ colors: colors });

      // Set currentColor initial value
      if (colors) {
        this.setState({ currentColor: Object.values(colors)[0] });
      }
    });
  }

  // TODO: Make popover work when window width is smaller than expected
  render() {
    return (
      <div className="p-1 text-left w-100 mx-auto dark-contrast w-75">
        <div className="p-3 w-100 h-100 bg-white">
          <Form onSubmit={this.handleSubmit}>
            <Form.Group controlId="config">
              <Form.Label>Script</Form.Label>
              <Form.Control as="select" disabled={this.state.solidColor}>
                {this.state.configs.map((name, idx) => {
                  return <option key={idx}>{name}</option>;
                })}
              </Form.Control>
            </Form.Group>

            <Form.Group controlId="solidColorCheck">
              <Form.Check
                value={this.state.solidColor}
                onChange={this.handleSolidColorCheck}
                label="Solid color"
              />
            </Form.Group>

            {this.state.solidColor ? (
              <React.Fragment>
                <Form.Label>Color entry</Form.Label>
                <Form.Row>
                  <Form.Group controlId="colorSelect" className="w-50 pr-1">
                    <Form.Control
                      as="select"
                      disabled={this.state.customColor}
                      onChange={this.handleColorSelect}
                    >
                      {Object.keys(this.state.colors).map((name, idx) => {
                        return <option key={idx}>{name}</option>;
                      })}
                    </Form.Control>
                  </Form.Group>
                  <Form.Group controlId="colorField" className="w-50 pl-1">
                    <Overlay
                      target={this.refs.colorField}
                      show={this.state.customColor}
                      placement="right"
                    >
                      <Popover>
                        <ChromePicker
                          color={this.state.currentColor}
                          onChange={e => this.updateCurrentColor(e.hex)}
                        />
                      </Popover>
                    </Overlay>
                    <Form.Control
                      ref="colorField"
                      type="text"
                      placeholder="#RRGGBB"
                      value={this.state.currentColor}
                      onChange={e => this.updateCurrentColor(e.target.value)}
                      disabled={!this.state.customColor}
                    />
                  </Form.Group>
                </Form.Row>

                <Form.Group controlId="customColorCheck">
                  <Form.Check
                    value={this.state.customColor}
                    onChange={this.handleCustomColorCheck}
                    label="Custom color"
                  />
                </Form.Group>
              </React.Fragment>
            ) : null}
            <div className="d-flex justify-content-end">
              <Form.Group
                controlId="submitButton"
                className="d-inline-block p-1 pb-0 mb-0"
              >
                <Button variant="primary" type="submit">
                  Submit
                </Button>
              </Form.Group>

              <Form.Group
                controlId="offButton"
                className="d-inline-block p-1 pb-0 mb-0"
              >
                <Button variant="danger" onClick={this.handleOff}>
                  Turn off
                </Button>
              </Form.Group>
            </div>
          </Form>
        </div>
      </div>
    );
  }

  /**
   * Update the currently entered color.
   * @param color - The new color
   */
  updateCurrentColor = color => {
    this.setState({ currentColor: color });
  };

  /**
   * Change whether the user can select a configuration or a solid color.
   * @param event - The change event from the checkbox
   */
  handleSolidColorCheck = event => {
    this.setState({ solidColor: event.target.checked });
  };

  /**
   * Update the currently entered color based on a select change event.
   * @param event - The change event from the select
   */
  handleColorSelect = event => {
    this.setState({ currentColor: this.state.colors[event.target.value] });
  };

  /**
   * Change whether the user can type the hex of a custom color or select from
   * the list of saved colors.
   * @param event - The change event from the checkbox
   */
  handleCustomColorCheck = event => {
    this.setState({ customColor: event.target.checked });
  };

  /**
   * Submit the form data.
   * @param event - The submit event
   */
  handleSubmit = event => {
    event.preventDefault();

    const target = event.currentTarget;

    let config, color;

    if (this.state.solidColor) {
      config = "solid_color";
    } else {
      config = target["config"].value;
    }

    if (this.state.customColor) {
      color = target["colorField"].value;
    } else if (target["colorSelect"]) {
      color = this.state.colors[target["colorSelect"].value];
    }

    const form = new FormData();
    form.set("config", config);
    form.set("color", color);

    axios
      .post("/submit", form)
      .then(response => console.log(response))
      .catch(error => console.log(error));
  };

  /**
   * Submit a request to turn off the lights.
   * @param event - The "Turn off" button event
   */
  handleOff = event => {
    event.preventDefault();

    const form = new FormData();
    form.set("config", "off");

    axios
      .post("/submit", form)
      .then(response => console.log(response))
      .catch(error => console.log(error));
  };
}
