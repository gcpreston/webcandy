import React from 'react';
import ReactDOM from 'react-dom';
import {
    BrowserRouter as Router,
    Route,
    Switch,
    Redirect
} from 'react-router-dom';

import App from './pages/App';
import Login from './pages/Login';
import CreateAccount from './pages/CreateAccount';
import NotFound from './pages/NotFound';

import "bootstrap/dist/css/bootstrap.css";
import '../css/index.css';

// TODO: Going to /hello tries to load /hello/dist/bundle.js??
const router = (
    <Router>
        <div>
            <Switch>
                <Route exact path="/" render={() => {
                    // App will redirect back to login if token has expired
                    return sessionStorage.getItem("token") !== null ? <App/> : <Redirect to="/login"/>;
                }}/>
                <Route path="/login" component={Login}/>
                <Route path="/create-account" component={CreateAccount}/>
                <Route component={NotFound}/>
            </Switch>
        </div>
    </Router>
);

ReactDOM.render(router, document.getElementById("content"));
