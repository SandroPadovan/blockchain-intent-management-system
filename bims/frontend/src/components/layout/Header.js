import React, {Component} from "react";
import PropTypes from "prop-types";
import { connect } from 'react-redux';
import { logout } from "../../actions/auth";
import { Link } from 'react-router-dom';


class Header extends Component {

    static propTypes = {
        auth: PropTypes.object.isRequired,
        logout: PropTypes.func.isRequired,
    }

    render() {
        const { isAuthenticated, user} = this.props.auth;

        const LoggedIn = (
            <div className="w-100 d-flex justify-content-end">
                <ul className="navbar-nav">
                    <li className="nav-item p-10">
                        <Link className="nav-link" to="/overview">Intents</Link>
                    </li>
                    <li className="nav-item">
                        <Link className="nav-link" to="/help">Help</Link>
                    </li>
                    <li className="nav-item dropdown">
                        <a className="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button"
                           aria-haspopup="true" aria-expanded="false">{user ? user.username : ''}</a>
                        <div className="dropdown-menu">
                            <a className="dropdown-item" onClick={this.props.logout}>logout</a>
                        </div>
                    </li>
                </ul>
            </div>
        );

        const notLoggedIn = (
            <div className="w-100 d-flex justify-content-end">
                <ul className="navbar-nav">
                    <li className="nav-item p-10">
                        <Link className="nav-link" to="/register">Register</Link>
                    </li>
                    <li className="nav-item">
                        <Link className="nav-link" to="/login">Login</Link>
                    </li>
                </ul>
            </div>
        );

        return (
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <a className="navbar-brand" href="/">BIMS</a>

                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#header"
                        aria-controls="navbarColor03" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"/>
                </button>
                <div className="collapse navbar-collapse" id="header">
                    {isAuthenticated ? LoggedIn : notLoggedIn}
                </div>
            </nav>
        );
    }
}

const mapStateToProps = (state) => ({
    auth: state.auth,
});

export default connect(mapStateToProps, { logout })(Header);
