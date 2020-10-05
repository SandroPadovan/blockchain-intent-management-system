import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {getPolicies} from '../../actions/intentActions'


class Policies extends Component {

    static propTypes = {
        policies: PropTypes.array.isRequired,
        selectedIntent: PropTypes.object.isRequired,
        getPolicies: PropTypes.func.isRequired,
    }

    componentDidMount() {
        if (this.props.selectedIntent.id) {
            this.props.getPolicies(this.props.selectedIntent.id);
        }
    }

    render() {
        return (
            <div className="row mt-4">
                {this.props.policies.map((policy, index) => (
                    <div key={policy.id} className="col-lg-6">
                        <div className="card text-white bg-secondary mb-3">
                            <div className="card-header">Policy {index + 1}</div>
                            <div className="card-body">
                                <div className="row">
                                    <div className="col-sm-4">User:</div>
                                    <div className="col-sm-8">{policy.user}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Cost Profile:</div>
                                    <div className="col-sm-8">{policy.cost_profile}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Timeframe Start:</div>
                                    <div className="col-sm-8">{policy.timeframe_start}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Timeframe End:</div>
                                    <div className="col-sm-8">{policy.timeframe_end}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Interval:</div>
                                    <div className="col-sm-8">{policy.interval}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Currency:</div>
                                    <div className="col-sm-8">{policy.currency_id}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Threshold:</div>
                                    <div className="col-sm-8">{policy.threshold}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Split Transactions:</div>
                                    <div className="col-sm-8">{policy.split_txs ? 'True' : 'False'}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Blockchain Pool:</div>
                                    <div className="col-sm-8">{policy.blockchain_pool == '' ? 'All' :
                                        <ul>{Object.values(policy.blockchain_pool).map(bc => (
                                            <li key={bc}>{bc}</li>))}
                                        </ul>}
                                    </div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Blockchain Type:</div>
                                    <div className="col-sm-8">{policy.blockchain_type}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Min. Trans. Rate:</div>
                                    <div className="col-sm-8">{policy.min_tx_rate}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Max. Block Time:</div>
                                    <div className="col-sm-8">{policy.max_block_time}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Min. Data Size:</div>
                                    <div className="col-sm-8">{policy.min_data_size}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Max. Trans. Cost:</div>
                                    <div className="col-sm-8">{policy.max_tx_cost}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Min. Popularity:</div>
                                    <div className="col-sm-8">{policy.min_popularity}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Min. Stability:</div>
                                    <div className="col-sm-8">{policy.min_stability}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Turing Complete:</div>
                                    <div className="col-sm-8">{policy.turing_complete ? 'True' : 'False'}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Encryption:</div>
                                    <div className="col-sm-8">{policy.encryption ? 'True' : 'False'}</div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-4">Redundancy:</div>
                                    <div className="col-sm-8">{policy.redundancy ? 'True' : 'False'}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        );
    }
}

const mapStateToProps = (state) => ({
    selectedIntent: state.intentReducer.selectedIntent,
    policies: state.intentReducer.policies,
});

export default connect(mapStateToProps, {getPolicies})(Policies);