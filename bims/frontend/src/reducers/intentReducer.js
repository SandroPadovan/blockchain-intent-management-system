import { GET_INTENTS, RETRIEVE_INTENT } from '../actions/types.js';

const initialState = {
    intents: [],
    selectedIntent: null
}

export default function (state = initialState, action) {
    switch (action.type) {
        case GET_INTENTS:
            return {
                ...state,
                selectedIntent: null,
                intents: action.payload
            }
        case RETRIEVE_INTENT:
            return {
                ...state,
                selectedIntent: action.payload
            }
        default:
            return state;
    }
}
