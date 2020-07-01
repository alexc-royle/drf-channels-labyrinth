import { useSelector } from 'react-redux';
import { getShape } from '../reducers';

import useGetShapesLoaded from './useGetShapesLoaded';
import useGetShapesLoading from './useGetShapesLoading';
import useLoadShapes from './useLoadShapes';

const useGetShape = ({ shapeId }) => {
  const shapesLoaded = useGetShapesLoaded();
  const shapesLoading = useGetShapesLoading();
  useLoadShapes({ shapesLoaded, shapesLoading });
  return useSelector(state => getShape(state, shapeId));
}

export default useGetShape;
