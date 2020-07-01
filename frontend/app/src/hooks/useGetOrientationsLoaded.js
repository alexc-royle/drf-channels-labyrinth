import { useSelector } from 'react-redux';
import { getOrientationsLoaded } from '../reducers';

const useGetOrientationsLoaded = () => {
  return useSelector(state => getOrientationsLoaded(state));
}

export default useGetOrientationsLoaded;
