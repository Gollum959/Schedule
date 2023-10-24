import { combineReducers } from 'redux';
import citiesReducer from './citiesReducer'; // Assuming you have a citiesReducer
import placesReducer from './placesReducer'

const rootReducer = combineReducers({
    cities: citiesReducer,
    places: placesReducer,
    // Add other reducers here if you have more
});

export default rootReducer;

