import axios from 'axios';
import {
    USER_LOADED,
    USER_LOADING,
    AUTH_ERROR,
    LOGIN_FAIL,
    LOGIN_SUCCESS,
    LOGOUT_SUCCESS,
    REGISTER_SUCCESS,
    REGISTER_FAIL
} from "./types";

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
        }).catch(err => {
            dispatch({
                type: AUTH_ERROR
            })
    })

}



// Login
export const login = (username, password) => dispatch => {

    const config = {
        headers: {
            "Content-Type": "application/json",
        }
    };

    const body = JSON.stringify({ username, password});

    axios
        .post("/api/auth/login", body, config)
        .then((res) => {
            dispatch({
                type: LOGIN_SUCCESS,
                payload: res.data,
            });
        })
        .catch((err) => {
            console.log(err);
            dispatch({
                type: LOGIN_FAIL,
            })
        })
}

// Logout
export const logout = () => (dispatch, getState) => {

    axios.post('/api/auth/logout', null, constructHeaders(getState))
        .then((res) => {
            dispatch({ type: LOGOUT_SUCCESS });
        })
        .catch((err) => {
            console.log(err);
        })
}

// Register
export const register = (username, password) => (dispatch, getState) => {
    const config = {
        headers: {
            'Content-Type': 'application/json',
        }
    }
    const body = JSON.stringify({username, password})

    axios.post('/api/auth/register', body, config)
        .then((res) => {
            console.log('hello world');
            dispatch({
                type: REGISTER_SUCCESS,
                payload: res.data
            });
        })
        .catch((err) => {
            dispatch({ type: REGISTER_FAIL });
        })
}