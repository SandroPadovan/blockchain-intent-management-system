import React, {Component} from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { login} from "../../actions/auth";

class Login extends Component {
    state = {
        username: "",
        password: ""
    }

    static propTypes = {
        login: PropTypes.func.isRequired,
        isAuthenticated: PropTypes.bool
    }

    onSubmit = e => {
        e.preventDefault();
        this.props.login(this.state.username, this.state.password);
    }

    onChange = e => this.setState({ [e.target.name]: e.target.value });

    render() {
        const {username, password} = this.state;
        return (
            <div>
                <form onSubmit={this.onSubmit}>
                    <div>
                        <label>Username</label>
                        <input
                            type="text"
                            name="username"
                            value={username}
                            onChange={this.onChange}
                        />
                    </div>
                    <div>
                        <label>Password</label>
                        <input
                            type="text"
                            name="password"
                            value={password}
                            onChange={this.onChange}
                        />
                    </div>
                    <div>
                        <button type="submit">Login</button>
                    </div>
                </form>
            </div>
        );
    }
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
})

export default connect(mapStateToProps, { login })(Login);