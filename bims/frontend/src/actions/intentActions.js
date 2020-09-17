import axios from 'axios';
import { constructHeaders } from "./auth";
import { createMessage, returnErrors } from "./messageActions";

import {
    GET_INTENTS,
    RETRIEVE_INTENT,
    DELETE_INTENT,
    LOADING,
    INTENT_ERROR,
    POLICY_SUCCESS,
    POLICY_FAIL,
    CREATE_INTENT,
    UPDATE_INTENT,
} from './types';

// GET intents
export const getIntents = () => (dispatch, getState) => {
    dispatch({ type: LOADING });

    axios.get('/api/intents/', constructHeaders(getState))
        .then(res => {
            dispatch({
                type: GET_INTENTS,
                payload: res.data
            })
        }).catch(err => dispatch(returnErrors(err.response.data, err.response.status)));
}


// Retrieve an intent
export const retrieveIntent = (id) => (dispatch, getState) => {
    dispatch({ type: LOADING });

    axios.get(`/api/intents/${id}`, constructHeaders(getState))
        .then(res => {
            dispatch({
                type: RETRIEVE_INTENT,
                payload: res.data
            })
        }).catch(err => {
            dispatch({
                type: INTENT_ERROR
            })
    });
}

export const deleteIntent = (id) => (dispatch, getState) => {

    axios.delete(`/api/intents/${id}`, constructHeaders(getState))
        .then(res => {
            dispatch(createMessage({deleteIntent: 'Intent deleted'}));
            dispatch({
                type: DELETE_INTENT
            })
        }).catch(err => {
            console.log(err);
    })
}


export const getPolicies = (id) => (dispatch, getState) => {

    axios.get(`/api/policies?intent_id=${id}`, constructHeaders(getState))
        .then(res => {
            dispatch({
                type: POLICY_SUCCESS,
                payload: res.data
            })
        }).catch(err => {
            dispatch({
                type: POLICY_FAIL
            })
    });
}

export const postIntent = (intent) => (dispatch, getState) => {

    const body = JSON.stringify({intent_string: intent});

    axios.post('/api/intents/', body, constructHeaders(getState))
        .then((res) => {
            dispatch(createMessage({createIntent: 'Intent created'}));
            dispatch({
                type: CREATE_INTENT,
                payload: res.data
            })
        })
        .catch((err) => dispatch(returnErrors(err.response.data, err.response.status)));
}

export const updateIntent = (id, new_intent) => (dispatch, getState) => {

    const body = JSON.stringify({intent_string: new_intent});

    axios.put(`/api/intents/${id}/`, body, constructHeaders(getState))
        .then(res => {
            dispatch(createMessage({updateIntent: 'Intent updated'}));
            dispatch({
                type: UPDATE_INTENT,
                payload: res.data
            })
        })
        .catch(err => dispatch(returnErrors(err.response.data, err.response.status)));

}

export const validateIntent = (intent) => {

    // dummy function
    return intent.length > 20;
}