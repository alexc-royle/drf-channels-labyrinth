import { useSelector } from 'react-redux';
import { getCollectableItem } from '../reducers';

const useGetGameCollectableItem = ({ collectableItemId }) => {
  return useSelector(state => getCollectableItem(state, collectableItemId));
}

export default useGetGameCollectableItem;
