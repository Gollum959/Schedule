// placesReducer.js
import {
    FETCH_PLACES_REQUEST,
    FETCH_PLACES_SUCCESS,
    FETCH_PLACES_FAILURE,
} from '../actions/placeActions';

const initialState = {
    places: [],
    loading: false,
    error: null,
};

const placesReducer = (state = initialState, action) => {
    switch (action.type) {
        case FETCH_PLACES_REQUEST:
            return {
                ...state,
                loading: true,
                error: null,
            };
        case FETCH_PLACES_SUCCESS:
            return {
                ...state,
                loading: false,
                places: action.payload,
                error: null,
            };
        case FETCH_PLACES_FAILURE:
            return {
                ...state,
                loading: false,
                error: action.payload,
            };
        default:
            return state;
    }
};

export default placesReducer;
