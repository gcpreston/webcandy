import React from 'react';
import ReactDOM from 'react-dom';
import {
    BrowserRouter as Router,
    Route,
    Switch,
    Redirect
} from 'react-router-dom';
import App from './components/App';
import Login from './components/Login';
import CreateAccount from './components/CreateAccount';
import NotFound from './components/NotFound';
import '../css/index.css';

function loggedIn() {
    // TODO: Make API call to check if token is still valid
   return Boolean(sessionStorage.getItem("token"));
}

const router = (
    <Router>
        <div>
            <Switch>
                <Route exact path="/" render={() => {
                    return loggedIn() ? <App/> : <Redirect to="/login"/>
                }}/>
                <Route path="/login" component={Login}/>
                <Route path="/create-account" component={CreateAccount}/>
                <Route component={NotFound}/>
            </Switch>
        </div>
    </Router>
);

ReactDOM.render(router, document.getElementById("content"));
