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
import NotFound from './components/NotFound';

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
                <Route component={NotFound}/>
            </Switch>
        </div>
    </Router>
);

ReactDOM.render(router, document.getElementById("content"));
