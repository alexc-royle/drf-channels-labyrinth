import { useEffect } from 'react';
import { useDispatch } from 'react-redux';

import { requestOrientations } from '../actions';

const useLoadOrientations = ({ orientationsLoaded, orientationsLoading }) => {
  const dispatch = useDispatch();
  useEffect(() => {
    console.log(orientationsLoaded, orientationsLoading);
    if (!orientationsLoaded && !orientationsLoading) {
      dispatch(requestOrientations());
    }
  }, [dispatch, orientationsLoaded, orientationsLoading]);
}

export default useLoadOrientations;
