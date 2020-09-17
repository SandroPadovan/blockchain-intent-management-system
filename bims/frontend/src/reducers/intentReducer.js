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
} from '../actions/types.js';

const initialState = {
    intents: [],
    selectedIntent: {},
    policies: [],
    isLoading: false
}

export default function (state = initialState, action) {
    switch (action.type) {
        case LOADING:
            return {
                ...state,
                selectedIntent: {},
                policies: [],
                isLoading: true,
            }
        case INTENT_ERROR:
            return {
                ...state,
                selectedIntent: null,
                policies: [],
                isLoading: false
            }
        case GET_INTENTS:
            return {
                ...state,
                selectedIntent: {},
                intents: action.payload,
                policies: [],
                isLoading: false
            }
        case RETRIEVE_INTENT:
            return {
                ...state,
                selectedIntent: action.payload,
                isLoading: false
            }
        case POLICY_SUCCESS:
            return {
                ...state,
                policies: action.payload,
                isLoading: false
            }
        case POLICY_FAIL:
            return {
                ...state,
                policies: [],
                isLoading: false
            }
        case CREATE_INTENT:
            return {
                ...state,
                intents: [...state.intents, action.payload],
                redirectToOverview: true,
            }
        case UPDATE_INTENT:
            return {
                ...state,
                selectedIntent: {},
                policies: [],
                isLoading: false,
                redirectToOverview: true,
            }
        case DELETE_INTENT:
            return {
                ...state,
                selectedIntent: null,
                isLoading: false
            }
        default:
            return state;
    }
}
