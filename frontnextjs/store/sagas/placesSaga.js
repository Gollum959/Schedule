// placeSaga.js
import { call, put, takeLatest } from 'redux-saga/effects';
import axios from 'axios';
import {
    FETCH_PLACES_REQUEST,
    fetchPlacesSuccess,
    fetchPlacesFailure,
} from '../actions/placeActions';

function* fetchPlaces(action) {
    try {
        const cityId = action.payload;
        const response = yield call(() => axios.get(`http://127.0.0.1:8000/api/v1/place/?city_id=${cityId}`));
        yield put(fetchPlacesSuccess(response.data));
    } catch (error) {
        yield put(fetchPlacesFailure(error));
    }
}

export function* watchFetchPlaces() {
    yield takeLatest(FETCH_PLACES_REQUEST, fetchPlaces);
}
