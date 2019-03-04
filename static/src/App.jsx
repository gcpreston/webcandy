import React from 'react';
import axios from 'axios';

export default class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      scripts: [],
    };
  }

  componentDidMount() {
    axios.get("/scripts").then(response => {
      this.setState({ scripts: response.data.scripts })
    });
  }

  render() {
    const buttons = this.state.scripts.map(s => {
      return <button key={s} onClick={this.handleClick(s)}>{s}</button>;
    });
    return <div id="buttons">{buttons}</div>;
  }

  handleClick(script) {
    return () => axios.get(`/run/${script}`)
        .then(response => console.log(response))
        .catch(error => console.log(error));
  }
}
