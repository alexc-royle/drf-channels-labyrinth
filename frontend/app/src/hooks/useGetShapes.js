import { useSelector } from 'react-redux';
import { getAllShapes } from '../reducers';

import useGetShapesLoaded from './useGetShapesLoaded';
import useGetShapesLoading from './useGetShapesLoading';
import useLoadShapes from './useLoadShapes';

const useGetShapes = () => {
  const shapesLoaded = useGetShapesLoaded();
  const shapesLoading = useGetShapesLoading();
  useLoadShapes({ shapesLoaded, shapesLoading });
  return useSelector(state => getAllShapes(state));
}

export default useGetShapes;
