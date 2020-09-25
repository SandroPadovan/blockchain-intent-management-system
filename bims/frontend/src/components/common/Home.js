import React, {Component} from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Link, Redirect } from 'react-router-dom';

class Home extends Component {

    static propTypes = {
            isAuthenticated: PropTypes.bool
    }

    render() {

        if (this.props.isAuthenticated) {
            return <Redirect to="/overview"/>
        }

        return (
            <div className="jumbotron d-flex align-items-center" style={{"backgroundColor": "transparent", "height": "75vh"}}>
                <div className="d-flex flex-column">
                    <div className="col-md-7">
                        <h1 className="display-3">Blockchain Intent Management System</h1>
                        <h3 className="mt-4">Intent-based Management for Blockchain Selection</h3>
                        <div className="d-flex flex-row mt-5">
                            <div>
                                <Link to="/login" className="btn btn-primary btn-lg mr-5">Sign in</Link>
                                <Link to="/register" className="btn btn-outline-primary btn-lg m-5">Sign up</Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state) => ({
    isAuthenticated: state.auth.isAuthenticated
});


export default connect(mapStateToProps)(Home);
