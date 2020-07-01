import { useSelector } from 'react-redux';
import { getAllOrientations } from '../reducers';

import useGetOrientationsLoaded from './useGetOrientationsLoaded';
import useGetOrientationsLoading from './useGetOrientationsLoading';
import useLoadOrientations from './useLoadOrientations';

const useGetOrientations = () => {
  const orientationsLoaded = useGetOrientationsLoaded();
  const orientationsLoading = useGetOrientationsLoading();
  useLoadOrientations({ orientationsLoaded, orientationsLoading });
  return useSelector(state => getAllOrientations(state));
}

export default useGetOrientations;
