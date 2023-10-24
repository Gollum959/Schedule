import { all } from 'redux-saga/effects';
import { watchFetchCities } from './citySaga';
import { watchFetchPlaces } from './placesSaga';

export default function* rootSaga() {
  yield all([
    watchFetchCities(),
    watchFetchPlaces(),
    // Add other sagas here
  ]);
}


