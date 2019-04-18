import React from 'react';
import ReactDOM from 'react-dom';
import { Route, Switch, BrowserRouter as Router } from 'react-router-dom';
import App from './App';
import NotFound from './components/NotFound';

class Hello extends React.Component {
    render() {
        return <p>Hello routing</p>
    }
}

const router = (
    <Router>
        <div>
            <Switch>
                <Route exact path="/" component={App}/>
                <Route path="/hello" component={Hello}/>
                <Route component={NotFound}/>
            </Switch>
        </div>
    </Router>
);

ReactDOM.render(router, document.getElementById("content"));
