import { useSelector } from 'react-redux';
import { getOrientationsLoading } from '../reducers';

const useGetOrientationsLoading = () => {
  return useSelector(state => getOrientationsLoading(state));
}

export default useGetOrientationsLoading;
