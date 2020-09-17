import React, {Component} from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { postIntent, validateIntent } from "../../actions/intentActions";
import { Link, Redirect } from 'react-router-dom';


class IntentCreation extends Component {

    state = {
        intent: "For ",
        isValid: false,
    }

    static propTypes = {
        postIntent: PropTypes.func.isRequired,
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
        this.props.postIntent(this.state.intent);
        this.props.history.goBack();
    }

    onChange = e => {
        this.setState({ [e.target.name]: e.target.value }, () => {
            this.checkIfValid();
        });
    }

    render() {

        const linkToHelp = <Link to="/help">Help Page</Link>
        const { intent } = this.state;

        return (
            <div>
                <Link to="/overview" className="btn btn-primary mt-4">Back</Link>
                <div className="jumbotron mt-4">
                    <h3>Create a new Intent</h3>
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
                            >Submit</button>
                        </div>
                    </form>
                    <p>For an explanation on how to create a valid Intent, see the {linkToHelp}</p>
                </div>
            </div>
        );
    }
}


export default connect(null, { postIntent })(IntentCreation);
