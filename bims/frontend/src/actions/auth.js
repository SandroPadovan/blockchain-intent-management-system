import axios from 'axios';
import {LOGIN_FAIL, LOGIN_SUCCESS} from "./types";

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