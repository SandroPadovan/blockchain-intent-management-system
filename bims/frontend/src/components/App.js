import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { HashRouter as Router, Route, Switch, Redirect } from 'react-router-dom';

import Intents from "./intents/Intents";
import Login from "./accounts/Login";

import { Provider } from 'react-redux';
import store from "../store";

class App extends Component {
    render() {
        return (
            <Provider store={store}>
                <Router>
                    <h1>Blockchain Intent Management System</h1>
                    <Switch>
                        <Route exact path="/login" component={Login} />
                    </Switch>
                </Router>
            </Provider>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('app'));