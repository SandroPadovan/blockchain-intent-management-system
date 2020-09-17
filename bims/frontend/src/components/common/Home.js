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
            <div className="jumbotron" style={{"backgroundColor": "transparent"}}>
                <h2 className="text-center">Blockchain Intent Management System</h2>
                <div className="col-md-6 m-auto">
                    <div className="card card-body mt-5 text-center">
                        <h4>Get started</h4>
                        <div className="m-5">
                            <Link to="/login" className="btn btn-primary btn-lg">Sign in</Link>
                        </div>
                        <div className="m-5">
                            <Link to="/register" className="btn btn-primary btn-lg">Sign up</Link>
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
