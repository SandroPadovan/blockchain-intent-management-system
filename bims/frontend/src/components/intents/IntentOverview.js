import React, {Component} from 'react';
import { getIntents } from "../../actions/intentActions";
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Moment from 'moment';

class IntentOverview extends Component {

    static propTypes = {
        intents: PropTypes.array.isRequired,
        getIntents: PropTypes.func.isRequired
    }

    componentDidMount() {
        this.props.getIntents();
    }

    render() {
        return (
            <div className="jumbotron" style={{"backgroundColor": "transparent"}}>
                <div className="d-flex justify-content-end">
                    <Link to="/create-intent" className="btn btn-primary">Create New Intent</Link>
                </div>
                <h2>Intent Overview</h2>
                {this.props.intents.length === 0 ?
                    <h4 className="mt-5">No intents yet...</h4>
                    :
                    <table className="table table-striped">
                        <thead>
                        <tr>
                            <th scope="col">Intent</th>
                            <th scope="col">Created at</th>
                            <th></th>
                        </tr>
                        </thead>
                        <tbody>
                        {this.props.intents.map((intent) => (
                            <tr key={intent.id}>
                                <td>{intent.intent_string}</td>
                                <td>{Moment(intent.created_at).format('DD.MM.YY HH:mm')}</td>
                                <td>
                                    <Link className="btn btn-secondary" to={`/intent/${intent.id}`}>Details</Link>
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                }
            </div>
        );
    }
}

const mapStateToProps = (state) => ({
    intents: state.intentReducer.intents,
});

export default connect(mapStateToProps, { getIntents })(IntentOverview);