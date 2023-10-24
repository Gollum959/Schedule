export const FETCH_CITIES_REQUEST = 'FETCH_CITIES_REQUEST';
export const FETCH_CITIES_SUCCESS = 'FETCH_CITIES_SUCCESS';
export const FETCH_CITIES_FAILURE = 'FETCH_CITIES_FAILURE';

export const fetchCitiesRequest = () => ({
  type: FETCH_CITIES_REQUEST,
});

export const fetchCitiesSuccess = (cities) => ({
  type: FETCH_CITIES_SUCCESS,
  payload: cities,
});

export const fetchCitiesFailure = (error) => ({
  type: FETCH_CITIES_FAILURE,
  payload: error,
});
