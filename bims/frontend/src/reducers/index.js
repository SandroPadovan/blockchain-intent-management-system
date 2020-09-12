import { combineReducers } from 'redux';
import auth from "./auth"
import intentReducer from "./intentReducer";

export default combineReducers({
    auth,
    intentReducer: intentReducer
});
