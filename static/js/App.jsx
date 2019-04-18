import React from 'react';
import LightConfigForm from './components/LightConfigForm';

export default class App extends React.Component {
    render() {
        return (
            <React.Fragment>
                <h1 id="title">Webcandy</h1>
                <LightConfigForm/>
            </React.Fragment>
        )
    }
}
