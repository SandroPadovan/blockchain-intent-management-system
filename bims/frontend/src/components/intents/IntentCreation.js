import React, {Component} from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { postIntent, validateIntent } from "../../actions/intentActions";
import { Link, Redirect } from 'react-router-dom';
import IntentInputField from "./IntentInputField";
import IntentExplanation from "./IntentExplanation";


class IntentCreation extends Component {

    constructor(props) {
        super(props);
        this.checkIfValid = this.checkIfValid.bind(this);
    }

    state = {
        isValid: false,
    }

    static propTypes = {
        redirectToOverview: PropTypes.bool.isRequired,
        postIntent: PropTypes.func.isRequired,
        expected: PropTypes.array.isRequired,
        parserMessage: PropTypes.string.isRequired,
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

    createIntent = (intent) => {
        this.props.postIntent(intent);
    }

    render() {
        if (this.props.redirectToOverview) {
            return <Redirect to="/overview"/>
        }

        const linkToHelp = <Link to="/help">Help Page</Link>

        return (
            <div>
                <Link to="/overview" className="btn btn-primary mt-4">Back</Link>
                <div className="jumbotron mt-4">
                    <h3>Create a new Intent</h3>
                    <IntentInputField
                        expected={this.props.expected}
                        checkIfValid={this.checkIfValid}
                        isValid={this.state.isValid}
                        onSubmit={this.createIntent}
                        buttonText="Submit"
                        initialValue="For "
                        parserMessage={this.props.parserMessage}
                    />
                    <IntentExplanation/>
                </div>
            </div>
        );
    }
}

const mapStateToProps = state => ({
    redirectToOverview: state.intentReducer.redirectToOverview,
    expected: state.intentReducer.expected,
    parserMessage: state.intentReducer.parserMessage,
})


export default connect(mapStateToProps, { postIntent, validateIntent })(IntentCreation);
