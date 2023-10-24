// placeActions.js
export const FETCH_PLACES_REQUEST = 'FETCH_PLACES_REQUEST';
export const FETCH_PLACES_SUCCESS = 'FETCH_PLACES_SUCCESS';
export const FETCH_PLACES_FAILURE = 'FETCH_PLACES_FAILURE';

export const fetchPlacesRequest = (cityId) => ({
    type: FETCH_PLACES_REQUEST,
    payload: cityId,
});

export const fetchPlacesSuccess = (places) => ({
    type: FETCH_PLACES_SUCCESS,
    payload: places,
});

export const fetchPlacesFailure = (error) => ({
    type: FETCH_PLACES_FAILURE,
    payload: error,
});
