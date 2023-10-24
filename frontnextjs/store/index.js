import { createStore, applyMiddleware } from 'redux';
import createSagaMiddleware from 'redux-saga';
import rootReducer from './reducers'; // Assuming you have a rootReducer
import rootSaga from './sagas'; // Create this file for your saga

const sagaMiddleware = createSagaMiddleware();
const store = createStore(rootReducer, applyMiddleware(sagaMiddleware));

sagaMiddleware.run(rootSaga);

export default store;
