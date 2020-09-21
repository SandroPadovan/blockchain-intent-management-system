import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Link, Redirect } from 'react-router-dom';
import { updateIntent, validateIntent } from '../../actions/intentActions';
import IntentInputField from "./IntentInputField";


class IntentEdit extends Component {

    constructor(props) {
        super(props);
        this.checkIfValid = this.checkIfValid.bind(this);
    }

    state = {
        isValid: true,
    }

    static propTypes = {
        intentReducer: PropTypes.object.isRequired,
        updateIntent: PropTypes.func.isRequired,
    }

    checkIfValid(intent) {
        this.props.validateIntent(intent)
            .then(valid => {    // resolve the Promise to the boolean whether the Intent is valid.
                if (intent && valid) {
                    this.setState({isValid: true});
                } else {
                    this.setState({isValid: false});
                }
            }).catch(err => console.log(err))
    }

    updateIntent = (intent) => {
        if (this.props.intentReducer.selectedIntent.intent_string !== intent) {
            this.props.updateIntent(this.props.intentReducer.selectedIntent.id, intent);
        }
    }

    render() {

        const linkToHelp = <Link to="/help">Help Page</Link>;
        const { redirectToOverview } = this.props.intentReducer;

        if (redirectToOverview) {
            return <Redirect to="/overview"/>;
        }

        return (
            <div>
                <button onClick={() => this.props.history.goBack()} className="btn btn-primary mt-4">Back</button>
                <div className="jumbotron mt-4">
                    <h3>Edit Intent</h3>
                    <IntentInputField
                        expected={this.props.intentReducer.expected}
                        checkIfValid={this.checkIfValid}
                        isValid={this.state.isValid}
                        onSubmit={this.updateIntent}
                        buttonText="Update"
                        initialValue={this.props.intentReducer.selectedIntent.intent_string}
                    />
                    <p>For an explanation on how to create a valid Intent, see the {linkToHelp}</p>
                </div>
            </div>
        );
    }
}

const mapStateToProps = state => ({
    intentReducer: state.intentReducer,
});


export default connect(mapStateToProps, { updateIntent, validateIntent })(IntentEdit);
