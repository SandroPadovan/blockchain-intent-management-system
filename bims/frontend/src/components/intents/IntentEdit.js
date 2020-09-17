import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Link, Redirect } from 'react-router-dom';
import { updateIntent, validateIntent } from '../../actions/intentActions';


class IntentEdit extends Component {

    state = {
        intent: "",
        isValid: true,
    }

    static propTypes = {
        intentReducer: PropTypes.object.isRequired,
        updateIntent: PropTypes.func.isRequired,
    }

    componentDidMount() {
        this.setState({intent: this.props.intentReducer.selectedIntent.intent_string});
    }

    checkIfValid() {
        if (validateIntent(this.state.intent)) {
            this.setState({isValid: true});
        } else {
            this.setState({isValid: false});
        }
    }

    onSubmit = e => {
        e.preventDefault();
        if (this.props.intentReducer.selectedIntent.intent_string !== this.state.intent) {
            this.props.updateIntent(this.props.intentReducer.selectedIntent.id, this.state.intent);
        }
    }

    onChange = e => {
        this.setState({ [e.target.name]: e.target.value }, () => {
            this.checkIfValid();
        });
    }

    render() {

        const linkToHelp = <Link to="/help">Help Page</Link>;
        const { intent } = this.state;
        const { redirectToOverview } = this.props.intentReducer;

        if (redirectToOverview) {
            return <Redirect to="/overview"/>;
        }

        return (
            <div>
                <button onClick={() => this.props.history.goBack()} className="btn btn-primary mt-4">Back</button>
                <div className="jumbotron mt-4">
                    <h3>Edit Intent</h3>
                    <form onSubmit={this.onSubmit}>
                        {this.state.isValid ?
                            <div className="form-group has-success mt-5">
                                <input
                                    type="text"
                                    value={intent}
                                    name="intent"
                                    className="form-control is-valid"
                                    id="intentInput"
                                    onChange={this.onChange}
                                />
                                <div className="valid-feedback">Valid Intent</div>
                            </div>
                            :
                            <div className="form-group has-danger mt-5">
                                <input
                                    type="text"
                                    value={intent}
                                    name="intent"
                                    className="form-control is-invalid"
                                    id="intentInput"
                                    onChange={this.onChange}
                                />
                                <div className="invalid-feedback">Invalid Intent</div>
                            </div>}

                        <div className="text-right">
                            <button
                                type="submit"
                                className="btn btn-primary"
                                disabled={!this.state.isValid}
                            >Update</button>
                        </div>
                    </form>
                    <p>For an explanation on how to create a valid Intent, see the {linkToHelp}</p>
                </div>
            </div>
        );
    }
}

const mapStateToProps = state => ({
    intentReducer: state.intentReducer,
});


export default connect(mapStateToProps, { updateIntent })(IntentEdit);
