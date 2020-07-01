import { useEffect } from 'react';
import { useDispatch } from 'react-redux';

import { requestShapes } from '../actions';

const useLoadShapes = ({ shapesLoaded, shapesLoading }) => {
  const dispatch = useDispatch();
  useEffect(() => {
    if (!shapesLoaded && !shapesLoading) {
      dispatch(requestShapes());
    }
  }, [dispatch, shapesLoaded, shapesLoading]);
}

export default useLoadShapes;
