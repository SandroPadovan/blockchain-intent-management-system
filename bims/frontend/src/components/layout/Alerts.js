import React, {Component, Fragment} from 'react';
import { withAlert } from 'react-alert';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';

class Alerts extends Component {

    static propTypes = {
        error: PropTypes.object.isRequired,
        message: PropTypes.object.isRequired
    }

    componentDidUpdate(prevProps) {
        const {error, message, alert} = this.props;

        if (error !== prevProps.error) {
            if (error.msg.expected) alert.error(`Invalid Intent.`);
            if (error.msg.non_field_errors) alert.error(error.msg.non_field_errors.join());
            if (error.msg.username) alert.error(`Username: ${error.msg.username.join()}`);
            if (error.msg.password) alert.error(`Password: ${error.msg.password.join()}`);

        }

        if (message !== prevProps.message) {
            if (message.deleteIntent) alert.success(message.deleteIntent);
            if (message.createIntent) alert.success(message.createIntent);
            if (message.passwordNotMatch) alert.error(message.passwordNotMatch);
            if (message.updateIntent) alert.success(message.updateIntent);
        }

    }

    render() {
        return <Fragment/>
    }
}

const mapStateToProps = state => ({
    error: state.errorReducer,
    message: state.messageReducer
})

export default connect(mapStateToProps)(withAlert()(Alerts));