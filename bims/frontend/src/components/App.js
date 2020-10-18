import React, {Component, Fragment} from 'react';
import ReactDOM from 'react-dom';
import {HashRouter as Router, Route, Switch} from 'react-router-dom';
import {Provider} from 'react-redux';

import Alerts from './layout/Alerts';
import Home from './common/Home';
import Help from './common/Help';
import IntentOverview from './intents/IntentOverview';
import IntentCreation from './intents/IntentCreation';
import IntentDetails from './intents/IntentDetails';
import IntentEdit from './intents/IntentEdit';
import Login from './accounts/Login';
import Register from './accounts/Register';
import Header from './layout/Header';
import PrivateRoute from './common/PrivateRoute';

import store from '../store';
import {loadUser} from '../actions/auth';

import {Provider as AlertProvider} from 'react-alert';
import AlertTemplate from 'react-alert-template-basic';

// Alert options
const alertOptions = {
    timeout: 7000,
    position: 'top center',
};

class App extends Component {

    componentDidMount() {
        store.dispatch(loadUser());
    }

    render() {
        return (
            <Provider store={store}>
                <AlertProvider template={AlertTemplate} {...alertOptions}>
                    <Router>
                        <Fragment>
                            <Header/>
                            <Alerts/>
                            <div className="container">
                                <Switch>
                                    <Route exact path="/" component={Home}/>
                                    <Route exact path="/login" component={Login}/>
                                    <Route exact path="/register" component={Register}/>
                                    <Route exact path="/help" component={Help}/>
                                    <PrivateRoute exact path="/overview" component={IntentOverview}/>
                                    <PrivateRoute exact path="/create-intent" component={IntentCreation}/>
                                    <PrivateRoute exact path="/intent/:id" component={IntentDetails}/>
                                    <PrivateRoute exact path="/intent/:id/edit" component={IntentEdit}/>
                                </Switch>
                            </div>
                        </Fragment>
                    </Router>
                </AlertProvider>
            </Provider>
        );
    }
}

ReactDOM.render(<App/>, document.getElementById('app'));