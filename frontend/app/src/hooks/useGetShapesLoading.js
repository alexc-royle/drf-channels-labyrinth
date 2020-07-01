import { useSelector } from 'react-redux';
import { getShapesLoading } from '../reducers';

const useGetShapesLoading = () => {
  return useSelector(state => getShapesLoading(state));
}

export default useGetShapesLoading;
