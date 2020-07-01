import { useSelector } from 'react-redux';
import { getShapesLoaded } from '../reducers';

const useGetShapesLoaded = () => {
  return useSelector(state => getShapesLoaded(state));
}

export default useGetShapesLoaded;
