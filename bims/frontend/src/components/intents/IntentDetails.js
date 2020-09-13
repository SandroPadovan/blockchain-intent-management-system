import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { retrieveIntent, deleteIntent } from "../../actions/intents";
import Moment from 'moment';
import Policies from "./Policies";
import { Link, Redirect } from 'react-router-dom';


class IntentDetails extends Component {

    static propTypes = {
        intentReducer: PropTypes.object.isRequired,
        isLoading: PropTypes.bool.isRequired,
        retrieveIntent: PropTypes.func.isRequired,
        deleteIntent: PropTypes.func.isRequired
    }

    componentDidMount() {
        this.props.retrieveIntent(this.props.match.params.id);
    }

    render() {
        const {selectedIntent, isLoading} = this.props.intentReducer;

        if (isLoading) {
            return <h2>Loading...</h2>
        } else if (selectedIntent) {
            const modal = (
                <div className="modal fade" id="confirmDelete">
                    <div className="modal-dialog" role="document">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title">Are you sure you want to delete this Intent?</h5>
                                <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div className="modal-footer">
                                <button type="button" className="btn btn-danger" data-dismiss="modal"
                                        onClick={() => {this.props.deleteIntent(selectedIntent.id)}}>Delete</button>
                                <button type="button" className="btn btn-secondary" data-dismiss="modal">Cancel</button>
                            </div>
                        </div>
                    </div>
                </div>
            )

            return (
                <div>
                    <Link to="/overview" className="btn btn-primary mt-4">Back</Link>
                    <div className="jumbotron mt-4">
                        <div className="row">
                            <div className="col-6">
                                <h3>Intent Details</h3>
                            </div>
                            <div className="col-6 text-right">
                                <Link to={`/intent/${selectedIntent.id}/edit`} className="btn btn-outline-primary m-3">Edit</Link>
                                <button className="btn btn-outline-danger m-3" data-toggle="modal"
                                        data-target="#confirmDelete">Delete</button>
                                {modal}
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-3">
                                <h5>Intent:</h5>
                            </div>
                            <div className="col-9">
                                <p>{selectedIntent.intent_string}</p>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-3">
                                <h5>Created at:</h5>
                            </div>
                            <div className="col-9">
                                <p>{Moment(selectedIntent.created_at).format('DD.MM.YY HH:mm')}</p>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-3">
                                <h5>Updated at:</h5>
                            </div>
                            <div className="col-9">
                                <p>{selectedIntent.created_at != selectedIntent.updated_at ?
                                    Moment(selectedIntent.updated_at).format('DD.MM.YY HH:mm')
                                    : '-'}</p>
                            </div>
                        </div>
                        <h5>Policies:</h5>
                        <Policies/>
                    </div>
                </div>
            );
        } else {
            return <Redirect to="/overview"/>
        }
    }
}

const mapStateToProps = (state) => ({
    intentReducer: state.intentReducer,
    isLoading: state.intentReducer.isLoading
});

export default connect(mapStateToProps, { retrieveIntent, deleteIntent })(IntentDetails);
