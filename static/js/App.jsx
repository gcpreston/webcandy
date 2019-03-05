import React from 'react';
import axios from 'axios';
import Dropdown from 'react-bootstrap/Dropdown';

export default class App extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      scripts: [],
    };
  }

  // TODO: Better way to do this?
  componentWillMount() {
    axios.get("/scripts").then(response => {
      this.setState({ scripts: response.data.scripts });
    });
  }

  render() {
    const menu = (
        <Dropdown.Menu>
          {this.state.scripts.map((name, idx) => {
            return (
                <Dropdown.Item key={idx} onClick={this.handleClick(name)}>
                  {name}
                </Dropdown.Item>
            );
          })}
        </Dropdown.Menu>
    );

    return (
      <Dropdown id="configs">
        <Dropdown.Toggle>
          Configurations
        </Dropdown.Toggle>
        {menu}
      </Dropdown>
    );
  }

  handleClick(script) {
    return () => axios.get(`/run/${script}`)
        .then(response => console.log(response))
        .catch(error => console.log(error));
  }
}
