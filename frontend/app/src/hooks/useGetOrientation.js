import { useSelector } from 'react-redux';
import { getOrientation } from '../reducers';

import useGetOrientationsLoaded from './useGetOrientationsLoaded';
import useGetOrientationsLoading from './useGetOrientationsLoading';
import useLoadOrientations from './useLoadOrientations';

const useGetOrientation = ({ orientationId }) => {
  return useSelector(state => getOrientation(state, orientationId));
}

export default useGetOrientation;
