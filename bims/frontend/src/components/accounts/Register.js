import React, {Component} from 'react';
import { Link, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { register } from "../../actions/auth";
import { createMessage } from "../../actions/messageActions";

class Register extends Component {
    state = {
        username: "",
        password: "",
        passwordConfirmation: "",
    }

    static propTypes = {
        register: PropTypes.func.isRequired,
        createMessage: PropTypes.func.isRequired,
        isAuthenticated: PropTypes.bool
    }

    onSubmit = e => {
        e.preventDefault();
        const { password, passwordConfirmation } = this.state;
        if (password !== passwordConfirmation) {
            this.props.createMessage({ passwordNotMatch: 'Passwords do not match' });
        } else {
            this.props.register(this.state.username, this.state.password);
        }
    }

    onChange = e => this.setState({ [e.target.name]: e.target.value });

    render() {
        if (this.props.isAuthenticated) {
            return <Redirect to="/overview"/>
        }
        const {username, password, passwordConfirmation} = this.state;
        return (
            <div>
                <div className="col-md-6 m-auto">
                    <div className="card card-body mt-5">
                        <h2 className="text-center">Register</h2>
                        <form onSubmit={this.onSubmit}>
                            <div className="form-group">
                                <label>Username</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    name="username"
                                    value={username}
                                    onChange={this.onChange}
                                />
                            </div>
                            <div className="form-group">
                                <label>Password</label>
                                <input
                                    type="password"
                                    className="form-control"
                                    name="password"
                                    value={password}
                                    onChange={this.onChange}
                                />
                            </div>
                            <div className="form-group">
                                <label>Confirm Password</label>
                                <input
                                    type="password"
                                    className="form-control"
                                    name="passwordConfirmation"
                                    value={passwordConfirmation}
                                    onChange={this.onChange}
                                />
                            </div>
                            <div>
                                <button
                                    type="submit"
                                    className="btn btn-primary"
                                >Create Account</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        );
    }
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
})

export default connect(mapStateToProps, { register, createMessage })(Register);