import { call, put, takeLatest } from 'redux-saga/effects';
import axios from 'axios';
import {
  FETCH_CITIES_REQUEST,
  fetchCitiesSuccess,
  fetchCitiesFailure,
} from '../actions/cities';

function* fetchCities() {
  try {
    const response = yield call(() => axios.get('http://127.0.0.1:8000/api/v1/city/'));
    yield put(fetchCitiesSuccess(response.data));
  } catch (error) {
    yield put(fetchCitiesFailure(error));
  }
}

export function* watchFetchCities() {
  yield takeLatest(FETCH_CITIES_REQUEST, fetchCities);
}
