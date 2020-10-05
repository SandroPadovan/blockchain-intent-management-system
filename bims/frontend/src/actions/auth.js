import axios from 'axios';
import {createMessage, returnErrors} from './messageActions';
import {
    USER_LOADED,
    USER_LOADING,
    AUTH_ERROR,
    LOGIN_FAIL,
    LOGIN_SUCCESS,
    LOGOUT_SUCCESS,
    REGISTER_SUCCESS,
    REGISTER_FAIL
} from './types';


// helper function: constructs header for requests (Content-Type + Authorization)
export const constructHeaders = (getState) => {
    const token = getState().auth.token;

    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    }
    if (token) {
        config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
}


export const loadUser = () => (dispatch, getState) => {
    // User loading
    dispatch({ type: USER_LOADING});

    axios.get('/api/auth/user', constructHeaders(getState))
        .then(res => {
            dispatch({
                type: USER_LOADED,
                payload: res.data
            })
        }).catch(() => {
            dispatch({
                type: AUTH_ERROR
            })
    })
}


export const login = (username, password) => (dispatch, getState) => {

    const body = JSON.stringify({ username, password});

    axios
        .post('/api/auth/login', body, constructHeaders(getState))
        .then((res) => {
            dispatch({
                type: LOGIN_SUCCESS,
                payload: res.data,
            });
        })
        .catch((err) => {
            dispatch(returnErrors(err.response.data, err.response.status));
            dispatch({
                type: LOGIN_FAIL,
            })
        })
}


export const logout = () => (dispatch, getState) => {

    axios.post('/api/auth/logout', null, constructHeaders(getState))
        .then(() => {
            dispatch(createMessage({logout: 'Successfully logged out'}));
            dispatch({ type: LOGOUT_SUCCESS });
        })
        .catch((err) => {
            console.log(err);
        })
}


export const register = (username, password) => (dispatch, getState) => {

    const body = JSON.stringify({username, password})

    axios.post('/api/auth/register', body, constructHeaders(getState))
        .then((res) => {
            dispatch({
                type: REGISTER_SUCCESS,
                payload: res.data
            });
        })
        .catch((err) => {
            dispatch(returnErrors(err.response.data, err.response.status));
            dispatch({ type: REGISTER_FAIL });
        })
}