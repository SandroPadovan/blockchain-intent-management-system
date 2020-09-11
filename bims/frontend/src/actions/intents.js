import axios from 'axios';
import { constructHeaders } from "./auth";

import {GET_INTENTS, RETRIEVE_INTENT} from './types';

// GET intents
export const getIntents = () => (dispatch, getState) => {

    axios.get('/api/intents/', constructHeaders(getState))
        .then(res => {
            dispatch({
                type: GET_INTENTS,
                payload: res.data
            })
        }).catch(err => console.log(err));
}


// Retrieve an intent
export const retrieveIntent = (id) => (dispatch, getState) => {

    axios.get(`/api/intents/${id}`, constructHeaders(getState))
        .then(res => {
            dispatch({
                type: RETRIEVE_INTENT,
                payload: res.data
            })
        }).catch(err => console.log(err));
}