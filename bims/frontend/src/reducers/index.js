import {combineReducers} from 'redux';
import auth from './auth'
import intentReducer from './intentReducer';
import errorReducer from './errorReducer';
import messageReducer from './messageReducer';

export default combineReducers({
    auth,
    intentReducer: intentReducer,
    errorReducer: errorReducer,
    messageReducer: messageReducer
});
